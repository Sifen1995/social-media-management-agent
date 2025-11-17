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

    async def execute_complete_pipeline(
        self,
        website_url: str,
        social_links: Dict[str, str],
        platforms: List[str],
        content_topics: List[str],
        credentials: Optional[Dict[str, Any]] = None,
        mode: str = "generate_only"  # generate_only, schedule, or post
    ) -> Dict[str, Any]:
        """
        Execute the complete multi-agent pipeline from brand research to content posting.

        Pipeline Steps:
        1. Scrape company information (brand_profile agent)
        2. Generate platform strategy (strategy agent)
        3. Generate text content (content agent)
        4. Generate graphics (graphics agent)
        5. Schedule or post content (poster agent)

        Args:
            website_url: Company website URL
            social_links: Dict of social media links
            platforms: Target platforms for content
            content_topics: List of content topics to generate
            credentials: Platform API credentials (required for posting)
            mode: Pipeline mode - generate_only, schedule, or post

        Returns:
            Complete pipeline results with all outputs
        """
        self.logger.info("Starting complete multi-agent pipeline")

        pipeline_results = {
            "started_at": self._get_timestamp(),
            "steps": {},
            "outputs": {
                "company_profile": None,
                "strategy_plan": None,
                "content_batch": None,
                "graphics": None,
                "posting_results": None
            },
            "status": "in_progress"
        }

        context = {
            "output_dir": "outputs",
            "pipeline_mode": mode
        }

        try:
            # Step 1: Scrape company information
            self.logger.info("Step 1/5: Scraping company information...")
            brand_task = {
                "website": website_url,
                "socials": social_links,
                "use_playwright": False
            }

            brand_result = await self.execute_task("brand_profile", brand_task, context)
            pipeline_results["steps"]["brand_profile"] = {
                "success": brand_result.get("success"),
                "completed_at": self._get_timestamp()
            }

            if not brand_result.get("success"):
                pipeline_results["status"] = "failed_at_brand_profile"
                pipeline_results["error"] = brand_result.get("message")
                return pipeline_results

            company_profile = brand_result.get("data")
            pipeline_results["outputs"]["company_profile"] = company_profile
            context["brand_profile"] = company_profile

            # Step 2: Generate platform strategy
            self.logger.info("Step 2/5: Generating platform strategy...")
            strategy_task = {
                "brand_profile": company_profile,
                "platforms": platforms,
                "mode": "comprehensive"
            }

            strategy_result = await self.execute_task("strategy", strategy_task, context)
            pipeline_results["steps"]["strategy"] = {
                "success": strategy_result.get("success"),
                "completed_at": self._get_timestamp()
            }

            if not strategy_result.get("success"):
                self.logger.warning("Strategy generation failed, continuing with defaults")
                strategy_plan = {}
            else:
                strategy_plan = strategy_result.get("data")
                pipeline_results["outputs"]["strategy_plan"] = strategy_plan
                context["strategy_plan"] = strategy_plan

            # Step 3: Generate text content for all topics and platforms
            self.logger.info("Step 3/5: Generating text content...")
            content_batch = []

            for topic in content_topics:
                for platform in platforms:
                    content_task = {
                        "platform": platform,
                        "action": "generate",
                        "topic": topic,
                        "content_type": "post",
                        "count": 3,
                        "brand_profile": company_profile,
                        "strategy_plan": strategy_plan
                    }

                    content_result = await self.execute_task("content", content_task, context)

                    if content_result.get("success"):
                        variations = content_result.get("data", [])
                        for variation in variations:
                            variation["platform"] = platform
                            variation["topic"] = topic
                            variation["id"] = f"{platform}_{topic}_{variation.get('variation', 1)}"
                            content_batch.append(variation)

            pipeline_results["steps"]["content_generation"] = {
                "success": len(content_batch) > 0,
                "items_generated": len(content_batch),
                "completed_at": self._get_timestamp()
            }

            pipeline_results["outputs"]["content_batch"] = content_batch

            # Save content batch to file
            self._save_content_batch(content_batch, context)

            # Step 4: Generate graphics
            self.logger.info("Step 4/5: Generating graphics...")
            graphics_results = []

            for content in content_batch[:10]:  # Limit to first 10 for demo
                graphics_task = {
                    "content": content,
                    "platform": content.get("platform"),
                    "mode": "specification",
                    "brand_profile": company_profile
                }

                graphics_result = await self.execute_task("graphics", graphics_task, context)

                if graphics_result.get("success"):
                    graphics_results.append(graphics_result.get("data"))

            pipeline_results["steps"]["graphics_generation"] = {
                "success": len(graphics_results) > 0,
                "items_generated": len(graphics_results),
                "completed_at": self._get_timestamp()
            }

            pipeline_results["outputs"]["graphics"] = graphics_results

            # Step 5: Post or schedule content
            if mode in ["schedule", "post"]:
                self.logger.info("Step 5/5: Posting/scheduling content...")

                poster_task = {
                    "content": content_batch,
                    "platforms": platforms,
                    "credentials": credentials or {},
                    "mode": mode
                }

                poster_result = await self.execute_task("poster", poster_task, context)
                pipeline_results["steps"]["posting"] = {
                    "success": poster_result.get("success"),
                    "completed_at": self._get_timestamp()
                }

                pipeline_results["outputs"]["posting_results"] = poster_result.get("data")
            else:
                self.logger.info("Step 5/5: Skipping posting (generate_only mode)")
                pipeline_results["steps"]["posting"] = {
                    "success": True,
                    "skipped": True,
                    "reason": "generate_only mode"
                }

            # Mark pipeline as complete
            pipeline_results["status"] = "completed"
            pipeline_results["completed_at"] = self._get_timestamp()

            # Generate summary report
            pipeline_results["summary"] = self._generate_pipeline_summary(pipeline_results)

            return pipeline_results

        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {str(e)}", exc_info=e)
            pipeline_results["status"] = "failed"
            pipeline_results["error"] = str(e)
            pipeline_results["failed_at"] = self._get_timestamp()
            return pipeline_results

    def _save_content_batch(self, content_batch: List[Dict[str, Any]], context: Dict[str, Any]) -> None:
        """Save content batch to JSON file."""
        try:
            import os
            import json

            output_dir = context.get("output_dir", "outputs")
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, "content_batch.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(content_batch, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Content batch saved to {output_path}")

        except Exception as e:
            self.logger.error(f"Failed to save content batch: {str(e)}")

    def _generate_pipeline_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of pipeline execution."""
        steps = results.get("steps", {})
        outputs = results.get("outputs", {})

        return {
            "total_steps": len(steps),
            "successful_steps": sum(1 for s in steps.values() if s.get("success")),
            "failed_steps": sum(1 for s in steps.values() if not s.get("success")),
            "content_items_generated": len(outputs.get("content_batch", [])),
            "graphics_generated": len(outputs.get("graphics", [])),
            "platforms_targeted": list(set(
                c.get("platform") for c in outputs.get("content_batch", [])
            )),
            "brand_name": outputs.get("company_profile", {}).get("brand_name", "Unknown"),
            "execution_time": self._calculate_execution_time(
                results.get("started_at"),
                results.get("completed_at")
            )
        }

    def _calculate_execution_time(self, start: Optional[str], end: Optional[str]) -> str:
        """Calculate execution time between two timestamps."""
        if not start or not end:
            return "Unknown"

        try:
            from datetime import datetime
            start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
            duration = end_dt - start_dt
            return f"{duration.total_seconds():.2f} seconds"
        except:
            return "Unknown"

    def _get_timestamp(self) -> str:
        """Get current UTC timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"


# Global orchestrator instance
orchestrator = AgentOrchestrator()
