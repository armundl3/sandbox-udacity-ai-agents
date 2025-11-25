"""Configuration management."""

import os
import sys
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel


class AgentConfig(BaseModel):
    """Configuration for the agent."""

    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    base_url: Optional[str] = None

    @classmethod
    def from_yaml(cls, path: str) -> "AgentConfig":
        """Load config from YAML file."""
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)


def load_config(config_path: Optional[str] = None) -> AgentConfig:
    """Load configuration from YAML file or use defaults."""
    if config_path and Path(config_path).exists():
        return AgentConfig.from_yaml(config_path)
    return AgentConfig()


def setup_environment() -> dict[str, str]:
    """
    Load environment variables from .env file.

    Returns:
        dict of loaded API keys
    """
    # Try to find .env in current dir or parent dirs
    possible_paths = [
        Path(".env"),
        Path(__file__).parent.parent / ".env",
        Path.cwd() / ".env",
    ]

    for path in possible_paths:
        if path.exists():
            load_dotenv(path)
            break

    # Collect API keys
    keys = {
        "tavily": os.getenv("TAVILY_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY") or os.getenv("VOCAREUM_OPENAI_API_KEY"),
    }

    # Validate required keys
    if not keys["tavily"]:
        print("Error: TAVILY_API_KEY not found in environment")
        print("Please set it in your .env file")
        sys.exit(1)

    return keys
