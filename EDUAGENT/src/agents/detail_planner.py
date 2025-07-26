import logging
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from src.clients.llm import LLMClient
from src.tools.tool import create_retrieve_tool
from src.state import State
from src.clients.databases import qdrant

logger = logging.getLogger(__name__)

class DetailPlannerPromptBuilder:
    def __init__(self):
        with open("D:\\EDUAGENT\\prompts\\src.agents.detail_planner.call.sp.txt", "r", encoding="utf-8") as file:
            self._prompt_template = file.read()

        with open("D:\\EDUAGENT\\prompts\\src.agents.detail_planner.call.um.txt", "r", encoding="utf-8") as file:
            self._user_message_template = file.read()
    
    def build(self, module_data, learner_profile, constraints):
        """Build prompt with module data from overview planner"""
        # Format the prompt with actual data
        formatted_prompt = self._prompt_template.format(
            module_title=module_data.get("title", ""),
            module_objectives=module_data.get("objectives", ""),
            duration_estimate=module_data.get("duration_estimate", ""),
            module_resources=module_data.get("resources", []),
            learner_level=learner_profile.get("level", "beginner"),
            preferred_study_style=learner_profile.get("preferred_study_style", ""),
            available_hours_per_day=constraints.get("available_hours_per_day", 2),
            available_days=constraints.get("available_days", ["Tuesday", "Sunday"])
        )
        
        user_message = self._user_message_template.format(
            conversation_context="Processing module for detailed planning",
            conversation=f"Please create detailed plan for module: {module_data.get('title', '')}"
        )
        
        return [
            SystemMessage(content=formatted_prompt),
            HumanMessage(content=user_message)
        ]

class DetailPlanner:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client 
        self.prompt_builder = DetailPlannerPromptBuilder()
    
    def process_single_module(self, module_data, learner_profile, constraints):
        """Process a single module from overview planner"""
        retrieve = create_retrieve_tool(
            vector_db=qdrant,
            retrieve_count=5,
        )
        
        def query_or_respond(state: MessagesState):
            """Generate tool call for retrieval or respond."""
            llm_with_tools = self.llm_client._llm.bind_tools([retrieve])
            response = llm_with_tools.invoke(state["messages"])
            return {"messages": [response]}

        def generate(state: MessagesState):
            """Generate detailed plan using retrieved content."""
            # Get retrieved content
            recent_tool_messages = []
            for message in reversed(state["messages"]):
                if message.type == "tool":
                    recent_tool_messages.append(message)
                else:
                    break
            tool_messages = recent_tool_messages[::-1]

            # Format retrieved content
            docs_content = "\n\n".join(doc.content for doc in tool_messages)
            
            # Build enhanced prompt with retrieved knowledge
            enhanced_prompt = self.prompt_builder.build(module_data, learner_profile, constraints)
            
            if docs_content:
                knowledge_context = f"\n\nRetrieved Knowledge Context:\n{docs_content}\n"
                enhanced_prompt[0].content += knowledge_context

            response = self.llm_client.invoke(enhanced_prompt)
            return {"messages": [response]}

        # Build sub-graph for processing
        tools = ToolNode([retrieve])
        graph_builder = StateGraph(MessagesState)
        
        graph_builder.add_node("query_or_respond", query_or_respond)
        graph_builder.add_node("tools", tools)
        graph_builder.add_node("generate", generate)

        graph_builder.set_entry_point("query_or_respond")
        graph_builder.add_conditional_edges(
            "query_or_respond",
            tools_condition,
            {END: END, "tools": "tools"},
        )
        graph_builder.add_edge("tools", "generate")
        graph_builder.add_edge("generate", END)

        return graph_builder.compile()

    def __call__(self, state):
        """Main entry point - process all modules from overview planner"""
        processed_modules = state.get("processed_modules", [])
        messages = state.get("messages", [])
        
        if not processed_modules:
            logger.warning("No processed modules found in state")
            return {"messages": messages + [HumanMessage(content="No modules to process")]}