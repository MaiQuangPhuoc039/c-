from flask import Flask, request, jsonify
from flask_cors import CORS
# from openai import OpenAI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..","..")))
from pydantic_settings import BaseSettings
from src.clients.llm import LLMClient
from langchain_core.messages import HumanMessage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.state import AgentProfile , State 
from src.agents.profile_collector import ProfileCollector
from langchain_core.runnables import RunnableConfig

app = Flask(__name__)
CORS(app)  # Cho phép truy cập từ frontend

llm_client=LLMClient(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_provider="groq"
)

agent = ProfileCollector(llm_client)
profile_agent = agent(State)

@app.route("/chat", methods=["POST"])
def chat():
        
        print('===== bắt dau =======')
        data = request.get_json()
        user_message = data.get("message", "")

        while True:
            print(f"đã nhận--: {user_message}")
            response = profile_agent.invoke(
                {"messages": user_message},
                config=RunnableConfig(configurable={"thread_id": "test_thread"})
            )

            ai_reply = response["messages"][-1].content if isinstance(response, dict) else response
            print(f"Hệ thống: {ai_reply}")
            
         
            if user_message.strip().lower() in ["exit", "quit", "q"]:
                break  
            return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(port=8000)