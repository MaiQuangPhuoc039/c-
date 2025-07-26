import logging
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.graph.state import CompiledStateGraph
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import time
from datetime import datetime
# from src.agents.detail_planner import DetailPlanner
from src.agents.profile_collector import ProfileCollector
from src.agents.overview_planner import OverViewPlanner

from src.clients.llm import LLMClient
from src.state import AgentProfile
from src.state import State

logger = logging.getLogger(__name__)

llm_client=LLMClient(model="meta-llama/llama-4-scout-17b-16e-instruct",api_provider="groq")

def run_overview_planner(state: State):
    """Check if profile is completed and ready for overview planning"""
    profile_completed = state.get("profile_completed", False)
    if profile_completed:
        return "overview_planner"
    return END

def process_overview_output(state: State):
    
    return 

def build_graph():
    graph = StateGraph(State)
    
    # Initialize agents
    profile_collector = ProfileCollector(llm_client=llm_client)
    overview_planner = OverViewPlanner(llm_client=llm_client)
    # detail_planner = DetailPlanner(llm_client=llm_client)

    # Add nodes
    graph.add_node("profile_collector", profile_collector)
    graph.add_node("overview_planner", overview_planner)
    # graph.add_node("detail_planner", detail_planner)
    graph.add_node("process_overview_output", process_overview_output)

    # Set up edges
    graph.add_edge(START, "profile_collector")
    
    # Conditional edge from profile collector
    graph.add_conditional_edges(
        "profile_collector",
        run_overview_planner,
        {END: END, "overview_planner": "overview_planner"},
    )
    # graph.add_edge("overview_planner", "process_overview_output")
    # graph.add_edge("process_overview_output", "detail_planner")
    # graph.add_edge("detail_planner", END)
    graph.add_edge("overview_planner", END)


    compiled_graph = graph.compile()
    return compiled_graph

build_graph()