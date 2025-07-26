import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph
from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from src.agents.profile_collector import ProfileCollector
from src.tools.tool import create_retrieve_tool
from src.state import State, StudyPlanOverview
# from src.clients.databases import qdrant
from src.clients.llm import LLMClient
from langchain_core.runnables import RunnableConfig


logger = logging.getLogger(__name__)

class OverviewPlannerPromptBuilder:
    def __init__(self):
        with open(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\prompts\src.agents.overview_planner.call.sp.txt", "r", encoding="utf-8") as file:
            self._prompt_template = file.read()

        with open(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\prompts\\src.agents.overview_planner.call.um.txt", "r", encoding="utf-8") as file:
            self._user_message_template = file.read()

    def build(self, state : State):
        user_message = state["messages"][-1].content
        variables = {
            "learning_goal": state["learning_goal"],
            "expected_result": state["expected_result"],
            "deadline": state["deadline"],
            "available_time": state["available_time"],
            "current_ability": state["current_ability"],
            "learning_obstacles": "\n".join(state["learning_obstacles"]),
            "learning_preference": state["learning_preference"],
            "specific_topics_interest": "\n".join(state["specific_topics_interest"]),
            "notes": state["notes"],
        }
        user_message = self._user_message_template.format(**variables)
        
        messages = [
            {"role": "system", "content": self._prompt_template},
            {"role": "user", "content": user_message},
        ]

        return ChatPromptTemplate.from_messages(messages)

class OverViewPlanner:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client 
        self.prompt_builder = OverviewPlannerPromptBuilder()
    
    async def __call__(self, state):
        # retrieve = create_retrieve_tool(
        #     vector_db=qdrant,
        #     retrieve_count=3,
        # )
        print(self.prompt_builder.build(state))
        response = await self.llm_client.ainvoke_with_retries(
            prompt=self.prompt_builder.build(state),
            output_model=StudyPlanOverview
        )

        return response
    
# if __name__ == "__main__":
        

#     llm_client=LLMClient(model="meta-llama/llama-4-scout-17b-16e-instruct",api_provider="groq")

#     agent_profile = ProfileCollector(llm_client)
#     profile_agent = agent_profile(State)


#     agent = OverViewPlanner(llm_client)
#     overview = agent(State)

#     response = overview.invoke({"messages":"tôi là Anh , tôi đang học lớp 10 , tôi muốn lên kế hoạch học môn toán để thi cuối kì, tôi muốn học 4 ngày trên tuần,và học 4 tiếng 1 ngày , tôi thích học theo video và giải bài tập thật nhiều"},
#         config=RunnableConfig(configurable={"thread_id": "test_thread"}))

#     response