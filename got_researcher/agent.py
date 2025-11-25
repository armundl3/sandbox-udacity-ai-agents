"""Agent and graph construction."""

from typing import Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from .config import AgentConfig
from .models import AgentState
from .prompts import get_system_prompt
from .tools import get_tools, init_tools


def create_llm(config: AgentConfig, api_key: Optional[str] = None) -> ChatOpenAI:
    """Create configured LLM instance."""
    kwargs = {
        "model": config.model,
        "temperature": config.temperature,
    }
    if config.base_url:
        kwargs["base_url"] = config.base_url
    if api_key:
        kwargs["api_key"] = api_key

    return ChatOpenAI(**kwargs)


def create_agent(config: AgentConfig, api_keys: dict[str, str]):
    """Create the research agent graph."""
    # Initialize tools
    init_tools(api_keys["tavily"])
    tools = get_tools()

    # Create LLM with tools
    llm = create_llm(config, api_keys.get("openai"))
    llm_with_tools = llm.bind_tools(tools)

    # Agent node
    def agent_node(state: AgentState):
        response = llm_with_tools.invoke(state.messages)
        return {"messages": [response]}

    # Router
    def router(state: AgentState):
        last_message = state.messages[-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return END

    # Build graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", router, ["tools", END])
    workflow.add_edge("tools", "agent")

    return workflow.compile()


def run_agent(
    query: str,
    config: AgentConfig,
    api_keys: dict[str, str],
    prompt_variant: str = "default",
) -> tuple[str, list]:
    """
    Run the agent with a query.

    Args:
        query: The user's question
        config: Agent configuration
        api_keys: Dictionary with 'tavily' and 'openai' keys
        prompt_variant: Which system prompt variant to use

    Returns:
        tuple of (final_response, all_messages)
    """
    graph = create_agent(config, api_keys)

    messages = [
        SystemMessage(content=get_system_prompt(prompt_variant)),
        HumanMessage(content=query),
    ]

    result = graph.invoke({"messages": messages})
    all_messages = result["messages"]

    # Extract final response
    final_response = ""
    for msg in reversed(all_messages):
        if isinstance(msg, AIMessage) and msg.content:
            final_response = msg.content
            break

    return final_response, all_messages
