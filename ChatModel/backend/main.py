from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_core import get_ai_response
import traceback

app = FastAPI(title="PakShop AI Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Backend running successfully"}

@app.post("/chat")
@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    try:
        reply = get_ai_response(request.message)
        return {"response": reply, "reply": reply}
    except Exception as e:
        # Exact error terminal par print hoga
        print("\n--- ERROR DETAILS START ---")
        traceback.print_exc()
        print("--- ERROR DETAILS END ---\n")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)