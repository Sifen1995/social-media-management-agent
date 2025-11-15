"""
Agent Orchestrator - coordinates multiple agents to complete complex tasks.
"""
from typing import Dict, Any, List, Optional
from app.agents.base.agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Orchestrates multiple agents to complete complex, multi-step tasks.

    The orchestrator:
    1. Maintains a registry of available agents
    2. Routes tasks to appropriate agents
    3. Manages agent execution flow
    4. Aggregates results from multiple agents
    """

    def __init__(self):
        """Initialize the orchestrator with an empty agent registry."""
        self._agents: Dict[str, BaseAgent] = {}
        self.logger = logging.getLogger(__name__)

    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register an agent with the orchestrator.

        Args:
            agent: Agent instance to register
        """
        agent_name = agent.name
        if agent_name in self._agents:
            self.logger.warning(f"Agent {agent_name} already registered. Overwriting.")

        self._agents[agent_name] = agent
        self.logger.info(f"Registered agent: {agent_name}")

    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """
        Get an agent by name.

        Args:
            agent_name: Name of the agent to retrieve

        Returns:
            Agent instance or None if not found
        """
        return self._agents.get(agent_name)

    def list_agents(self) -> List[Dict[str, str]]:
        """
        Get list of all registered agents.

        Returns:
            List of dicts with agent name and description
        """
        return [
            {
                "name": agent.name,
                "description": agent.description
            }
            for agent in self._agents.values()
        ]

    async def execute_task(
        self,
        agent_name: str,
        task: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a task using a specific agent.

        Args:
            agent_name: Name of the agent to use
            task: Task parameters
            context: Execution context

        Returns:
            Result from the agent
        """
        agent = self.get_agent(agent_name)

        if not agent:
            return {
                "success": False,
                "message": f"Agent '{agent_name}' not found",
                "data": None,
                "metadata": {"available_agents": [a.name for a in self._agents.values()]}
            }

        try:
            # Validate input
            is_valid = await agent.validate_input(task)
            if not is_valid:
                return {
                    "success": False,
                    "message": f"Invalid input for agent {agent_name}",
                    "data": None,
                    "metadata": {"required_fields": agent.get_required_fields()}
                }

            # Execute task
            await agent.pre_execute(task, context)
            result = await agent.execute(task, context)
            await agent.post_execute(result, task)

            return result

        except Exception as e:
            self.logger.error(f"Error executing task with {agent_name}: {str(e)}", exc_info=e)
            return {
                "success": False,
                "message": f"Error in {agent_name}: {str(e)}",
                "data": None,
                "metadata": {"error": str(e)}
            }

    async def execute_workflow(
        self,
        workflow: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Execute a multi-step workflow across multiple agents.

        Args:
            workflow: List of tasks, each with 'agent' and 'task' keys
            context: Shared context for all tasks

        Returns:
            List of results from each agent
        """
        results = []

        for step_num, step in enumerate(workflow, 1):
            agent_name = step.get("agent")
            task = step.get("task", {})

            self.logger.info(f"Executing workflow step {step_num}/{len(workflow)}: {agent_name}")

            result = await self.execute_task(agent_name, task, context)
            results.append({
                "step": step_num,
                "agent": agent_name,
                "result": result
            })

            # If a step fails and is marked as critical, stop the workflow
            if not result.get("success") and step.get("critical", False):
                self.logger.error(f"Critical step {step_num} failed. Stopping workflow.")
                break

            # Add result to context for next steps
            context[f"step_{step_num}_result"] = result.get("data")

        return results

    async def delegate_to_planner(
        self,
        user_request: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Delegate a user request to the Planner Agent for task decomposition.

        Args:
            user_request: Natural language request from user
            context: Execution context

        Returns:
            Result from planner agent with execution plan
        """
        planner = self.get_agent("planner")

        if not planner:
            return {
                "success": False,
                "message": "Planner agent not available",
                "data": None
            }

        task = {
            "user_request": user_request,
            "description": "Analyze and plan execution for user request"
        }

        return await self.execute_task("planner", task, context)


# Global orchestrator instance
orchestrator = AgentOrchestrator()
