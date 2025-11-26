"""LangChain tools for the agent."""

from typing import Optional

import requests
from langchain_core.tools import tool
from tavily import TavilyClient

from .models import GOTQuote, TavilyResponse

# Module-level client (set by init_tools)
_tavily_client: Optional[TavilyClient] = None


def init_tools(tavily_api_key: str) -> None:
    """Initialize tool dependencies."""
    global _tavily_client
    _tavily_client = TavilyClient(api_key=tavily_api_key)


@tool
def random_got_quote() -> GOTQuote:
    """Return a random Game of Thrones quote and the character who said it."""
    response = requests.get("https://api.gameofthronesquotes.xyz/v1/random")
    response.raise_for_status()
    return GOTQuote(**response.json())


@tool
def web_search(question: str) -> TavilyResponse:
    """Search the web for information. Returns top search results."""
    if _tavily_client is None:
        raise RuntimeError("Tools not initialized. Call init_tools() first.")
    response = _tavily_client.search(question)
    return TavilyResponse(**response)


def get_tools() -> list:
    """Get list of all available tools."""
    return [random_got_quote, web_search]
