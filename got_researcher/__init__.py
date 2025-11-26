"""Game of Thrones Quote Researcher Agent.

A modular LangGraph agent that fetches random Game of Thrones quotes
and researches the actors who played those characters.
"""

from .agent import create_agent, run_agent
from .config import AgentConfig, load_config, setup_environment
from .models import AgentState, GOTQuote, TavilyResponse

__version__ = "0.1.0"
__all__ = [
    "create_agent",
    "run_agent",
    "AgentConfig",
    "load_config",
    "setup_environment",
    "GOTQuote",
    "TavilyResponse",
    "AgentState",
]
