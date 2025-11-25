# sandbox-udacity-ai-agents

AI Agents with Langchain and LangGraph

## Project Overview

This repository contains exercises and demos for building AI agents using LangChain and LangGraph, including:

- Jupyter notebooks for learning and experimentation
- Modular Python CLI applications

## Setup

### Prerequisites

- Python 3.13+ (managed via pyenv)
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd sandbox-udacity-ai-agents

# Install dependencies
uv sync

# Activate virtual environment (optional, uv run handles this)
source .venv/bin/activate
```

### Environment Variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your-tavily-api-key
OPENAI_API_KEY=your-openai-api-key
# Or for Vocareum:
# VOCAREUM_OPENAI_API_KEY=your-vocareum-key
```

## GOT Researcher CLI

A modular LangGraph agent that fetches random Game of Thrones quotes and researches the actors who played those characters.

### Usage

```bash
# Basic usage - get a random quote with performer info
uv run python -m got_researcher "Give me a random GoT quote"

# With verbose output (shows full conversation)
uv run python -m got_researcher -v "Random quote please"

# With custom config file
uv run python -m got_researcher --config config.yaml "Who said 'Winter is coming'?"
```

### Configuration

Create an optional `config.yaml` file to customize the LLM:

```yaml
model: gpt-4o-mini
temperature: 0.0
# base_url: https://custom-endpoint.com/v1  # Optional
```

### Example Output

```
============================================================
RESULT
============================================================
Quote: "The things I do for love."
Character: Jaime Lannister
Performer: Nikolaj Coster-Waldau
```

### Package Structure

```
got_researcher/
├── __init__.py      # Package exports
├── __main__.py      # Entry point for python -m
├── cli.py           # Command line interface
├── config.py        # Configuration management
├── models.py        # Pydantic models
├── tools.py         # LangChain tools
├── agent.py         # Agent graph logic
└── prompts.py       # System prompts
```

### Using as a Library

```python
from got_researcher import run_agent, AgentConfig, setup_environment

# Setup
api_keys = setup_environment()
config = AgentConfig(model="gpt-4o-mini")

# Run
response, messages = run_agent(
    query="Give me a random GoT quote",
    config=config,
    api_keys=api_keys,
)

print(response)
```

## Notebooks

Located in `nb/` directory:

- `L3 Loan Agent Starter Exercise.ipynb` - Loan negotiation agent with LangGraph
- `L4 Demo 01 Calling APIs.ipynb` - API integration with tools

## Development

```bash
# Add a new dependency
uv add <package>

# Run a script
uv run python <script.py>

# Run Jupyter notebooks
uv run jupyter notebook
```
