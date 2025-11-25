"""Command line interface."""

import argparse

from .agent import run_agent
from .config import AgentConfig, load_config, setup_environment


def print_conversation(messages: list) -> None:
    """Print full conversation history."""
    print("\n" + "=" * 60)
    print("CONVERSATION HISTORY")
    print("=" * 60)
    for msg in messages:
        msg.pretty_print()
    print("=" * 60 + "\n")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Game of Thrones Quote Researcher Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m got_researcher "Give me a random GoT quote"
    python -m got_researcher --config config.yaml "Random quote"
    python -m got_researcher -v "Who said Winter is coming?"
        """,
    )
    parser.add_argument("query", type=str, help="Question for the agent")
    parser.add_argument(
        "--config", "-c", type=str, default=None, help="Path to YAML config file"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show full conversation history"
    )

    args = parser.parse_args()

    # Setup
    api_keys = setup_environment()
    config = load_config(args.config)

    if args.verbose:
        print(f"Model: {config.model}")
        print(f"Query: {args.query}\n")

    # Run agent
    response, messages = run_agent(args.query, config, api_keys)

    if args.verbose:
        print_conversation(messages)

    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    print(response)


if __name__ == "__main__":
    main()
