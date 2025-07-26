import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.clients.llm import LLMClient
from src.state import AgentProfile , State  , StudyPlanOverview
from src.agents.profile_collector import ProfileCollector
from src.agents.overview_planner import OverViewPlanner

from langchain_core.runnables import RunnableConfig
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic_settings import BaseSettings
from langchain_core.messages import HumanMessage
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.configs import env_config




if __name__ == "__main__":
    # llm_client=LLMClient(model="meta-llama/llama-4-scout-17b-16e-instruct",api_provider="groq")
    llm_client=LLMClient(model=env_config.model  , api_provider=env_config.api_provider)

    agent_pro = ProfileCollector(llm_client)
    profile_agent = agent_pro(State)

    # agent_over = OverViewPlanner(llm_client)
    # overview_agent = agent_over(profile_agent)

    print("=== Bắt đầu hội thoại với hệ thống ===")
    user_input = input("Bạn: ")

    while True: 
        response = profile_agent.invoke(
            {"messages": user_input},
            config=RunnableConfig(configurable={"thread_id": "test_thread"})
        )

        ai_reply = response["messages"][-1].content if isinstance(response, dict) else response
        print(f"Hệ thống: {ai_reply}")
        # print(f"response: {response}")


        user_input = input("Bạn--: ")
        if user_input.strip().lower() in ["exit", "quit", "q"]:
            break
