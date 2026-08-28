from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ai_core.py file se function import kar rahe hain
from ai_core import get_ai_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
def chat(data: ChatRequest):
    # User ka message AI function ko bhej rahe hain
    print(f"Received message: {data.message}")
    reply = get_ai_response(data.message)
    return {"reply": reply}