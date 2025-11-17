"""
Agent Initialization Script

This script initializes and registers all agents with the orchestrator.
Import this module to get a fully configured orchestrator instance.
"""
import logging
from typing import Optional
from app.agents.base.orchestrator import AgentOrchestrator
from app.agents.brand_profile.agent import BrandProfileAgent
from app.agents.strategy.agent import StrategyAgent
from app.agents.content.agent import ContentAgent
from app.agents.graphics.agent import GraphicsAgent
from app.agents.poster.agent import PosterAgent
from app.agents.planner.agent import PlannerAgent
from app.agents.scheduler.agent import SchedulerAgent
from app.agents.analytics.agent import AnalyticsAgent
from app.agents.engagement.agent import EngagementAgent
from app.agents.social_listening.agent import SocialListeningAgent
from app.agents.optimizer.agent import OptimizerAgent
from app.services.llm_service import LLMService
from app.core.config import settings

logger = logging.getLogger(__name__)

# Global orchestrator instance
_orchestrator: Optional[AgentOrchestrator] = None


def get_llm_service() -> LLMService:
    """
    Create and configure LLM service.

    Returns:
        Configured LLM service instance
    """
    # LLMService reads configuration from settings automatically
    return LLMService()


def initialize_all_agents() -> AgentOrchestrator:
    """
    Initialize and register all agents with the orchestrator.

    Returns:
        Fully configured orchestrator with all agents registered
    """
    global _orchestrator

    if _orchestrator is not None:
        logger.info("Using existing orchestrator instance")
        return _orchestrator

    logger.info("Initializing orchestrator and agents...")

    # Create orchestrator
    orchestrator = AgentOrchestrator()

    # Create LLM service
    llm_service = get_llm_service()

    # Initialize all agents
    agents = [
        # Core pipeline agents (NEW)
        BrandProfileAgent(llm_service=llm_service),
        StrategyAgent(llm_service=llm_service),
        ContentAgent(llm_service=llm_service),
        GraphicsAgent(llm_service=llm_service),
        PosterAgent(llm_service=llm_service),

        # Supporting agents (EXISTING)
        PlannerAgent(llm_service=llm_service),
        SchedulerAgent(llm_service=llm_service),
        AnalyticsAgent(llm_service=llm_service),
        EngagementAgent(llm_service=llm_service),
        SocialListeningAgent(llm_service=llm_service),
        OptimizerAgent(llm_service=llm_service)
    ]

    # Register all agents
    for agent in agents:
        try:
            orchestrator.register_agent(agent)
            logger.info(f"✓ Registered {agent.name} agent")
        except Exception as e:
            logger.error(f"✗ Failed to register {agent.name} agent: {str(e)}")

    logger.info(f"Initialization complete. {len(orchestrator.list_agents())} agents registered.")

    # Cache the orchestrator
    _orchestrator = orchestrator

    return orchestrator


def get_orchestrator() -> AgentOrchestrator:
    """
    Get the global orchestrator instance, initializing if necessary.

    Returns:
        Orchestrator instance
    """
    global _orchestrator

    if _orchestrator is None:
        _orchestrator = initialize_all_agents()

    return _orchestrator


def list_registered_agents():
    """
    Print all registered agents and their descriptions.
    """
    orchestrator = get_orchestrator()
    agents = orchestrator.list_agents()

    print("\n" + "="*60)
    print("REGISTERED AGENTS")
    print("="*60)

    for idx, agent_info in enumerate(agents, 1):
        print(f"\n{idx}. {agent_info['name'].upper()}")
        print(f"   {agent_info['description']}")

    print("\n" + "="*60)
    print(f"Total: {len(agents)} agents")
    print("="*60 + "\n")


if __name__ == "__main__":
    # When run directly, initialize and list agents
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    orchestrator = initialize_all_agents()
    list_registered_agents()

    print("Orchestrator ready! Import with:")
    print("  from initialize_agents import get_orchestrator")
    print("  orchestrator = get_orchestrator()")
