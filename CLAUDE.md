# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Agents sandbox using Langchain and LangGraph for building conversational AI agents and workflows.

## Tech Stack

- Python
- Langchain: Framework for building LLM-powered applications
- LangGraph: Library for building stateful, multi-actor applications with LLMs

## Development Setup

Python version: 3.13.7 (managed by pyenv via `.python-version` file)
Package manager: uv
Virtual environment: `.venv` (managed by uv)

### Common Commands

- `uv sync` - Sync dependencies from uv.lock
- `uv add <package>` - Add a new dependency
- `uv run <command>` - Run command in virtual environment
- `uv pip install <package>` - Install package in current venv
- `source .venv/bin/activate` - Activate virtual environment manually

### Setup for New Contributors

```bash
# Python version is auto-selected via .python-version
# Install dependencies
uv sync

# Or manually activate the venv
source .venv/bin/activate
```

Environment variables for API keys (especially OpenAI) should be stored in `.env` (already gitignored)

## Architecture Notes

As this is a sandbox/learning repository for AI agents:
- Expect Jupyter notebooks for experimentation and tutorials
- Python scripts may be organized by agent type or use case
- Langchain agents typically use tools, memory, and chains for workflow orchestration
- LangGraph adds stateful graph-based workflows on top of Langchain
