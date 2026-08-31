from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from ai_core import get_ai_response

app = FastAPI()

@app.post("/api/chat")
def chat(data: dict):
    reply = get_ai_response(data.get("message", ""))
    return {"reply": reply}

# Frontend Static Files Serve Karna
frontend_dist = os.path.join(os.path.dirname(__file__), "../frontend/dist")

if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_react(full_path: str):
        return FileResponse(os.path.join(frontend_dist, "index.html"))