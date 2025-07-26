import json
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pathlib import Path
from typing import Type, Union
from langchain.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from src.clients.llm import LLMClient
from src.state import MiniTestState, ChapterLevel
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain.schema import HumanMessage , AIMessage, SystemMessage
from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition
logger = logging.getLogger(__name__)
from langgraph.graph import MessagesState, StateGraph
from src.tools.tool import create_parser_output_tool

llm_client=LLMClient(
        model="gpt-4o-mini",
        api_provider="openai",
    ) 

collect_tool = create_parser_output_tool(
    llm_client=llm_client,
    state=MiniTestState
)
class MiniTestPromptBuilder:
    """Agent responsible for collecting and managing user learning mini_test."""

    def __init__(self):
        with open(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\prompts\mini_test_sp.txt", "r",encoding="utf-8") as file:
            self._prompt_template = file.read()

        with open(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\prompts\mini_test_up.txt", "r", encoding="utf-8") as file:
            self._user_template = file.read()
    def build(self, state : MiniTestState) :
        return ChatPromptTemplate.from_messages([
            {"role": "system", "content": self._prompt_template},
            {"role": "user", "content": self._user_template}
        ])

class MiniTester:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client 
        self.prompt_builder = MiniTestPromptBuilder()

    def __call__(self, state: MiniTestState) -> dict:

        if state is None:
            state = MiniTestState(messages=[], grade="", chapter=[])

        try:
            prompt_template = self.prompt_builder.build(state)
                    
            def chat(state: MiniTestState):
                llm = self.llm_client._llm.bind_tools([collect_tool])
                messages = [
                    msg for msg in state["messages"]
                    if msg.type in ("human", "system") or (msg.type == "ai" and not msg.tool_calls)
                ]
                full_prompt = [SystemMessage(content=prompt_template.format())] + messages
                response = llm.invoke(full_prompt)
                return {"messages": [response]}
            
            # tools = ToolNode([collect_mini_test])

            def generate(state: MiniTestState):
                tool_messages = [
                    msg for msg in reversed(state["messages"]) if msg.type == "tool"
                ]
                last_tool = tool_messages[-1]
                return {
                    "mini_test": last_tool.artifact,
                    "messages": [AIMessage(content="Hồ sơ mini test đã hoàn thành.")]
                }

            builder = StateGraph(MiniTestState)
            builder.add_node(chat)
            builder.add_node(generate)

            builder.set_entry_point("chat")
            builder.add_conditional_edges("chat", tools_condition, {END: END, "tools": "generate"})
            builder.add_edge("generate", END)

            return builder.compile(checkpointer=MemorySaver())
            
        except Exception as e:
            logger.error(f"Error executing profile collector: {e}")
            raise RuntimeError(f"Profile collection failed: {e}")

if __name__ == "__main__":
    # llm_client = LLMClient(
    #     model="gpt-4o-mini",
    #     api_provider="openai",
    # )

    agent = MiniTester(llm_client)
    mini_test_agent = agent(MiniTestState)

    print("=== Bắt đầu hội thoại với hệ thống ===")
    user_input = input("Bạn_mini_test: ")

    while True:
        response = mini_test_agent.invoke(
            {"messages": user_input},
            config=RunnableConfig(configurable={"thread_id": "test_thread"})
        )

        ai_reply = response["messages"][-1].content if isinstance(response, dict) else response
        print(f"Hệ thống: {ai_reply}")

        user_input = input("Bạn_mini_test: ")
        if user_input.strip().lower() in ["exit", "quit", "q"]:
            break



    # llm_client = LLMClient(
    #     model="gpt-4o-mini",
    #     api_provider="openai",
    # )

    # agent = MiniTester(llm_client)
    # profile_agent = agent(MiniTestState)

    # response = profile_agent.invoke({"messages":"hi"}, config=RunnableConfig(
    #     configurable={"thread_id": "test_thread"}))

    # response