from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Cho phép FE gọi BE từ localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sau này nên giới hạn lại
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    user_msg = req.message.strip()

    # Phản hồi đơn giản hoặc dùng LLM thật tại đây
    response = f"Tôi đã nhận được: '{user_msg}'. Đây là phản hồi mẫu."
    
    return {"response": response}
