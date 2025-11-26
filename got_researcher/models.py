"""Pydantic models for API responses and agent state."""

from typing import Annotated, List, Optional

from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


# =============================================================================
# Game of Thrones API Models
# =============================================================================


class House(BaseModel):
    """Game of Thrones house."""

    name: str
    slug: str


class Character(BaseModel):
    """Game of Thrones character."""

    name: str
    slug: str
    house: House


class GOTQuote(BaseModel):
    """A quote from Game of Thrones."""

    sentence: str
    character: Character


# =============================================================================
# Tavily Search Models
# =============================================================================


class SearchResult(BaseModel):
    """A single search result from Tavily."""

    title: str
    url: str
    content: str
    score: float
    raw_content: Optional[str] = None


class TavilyResponse(BaseModel):
    """Response from Tavily search API."""

    query: str
    follow_up_questions: Optional[List[str]] = None
    answer: Optional[str] = None
    images: List[str] = Field(default_factory=list)
    results: List[SearchResult]
    response_time: float


# =============================================================================
# Agent State
# =============================================================================


class AgentState(BaseModel):
    """State for the research agent."""

    messages: Annotated[list, add_messages] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True
