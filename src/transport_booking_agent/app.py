from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .graph.orchestrator import GraphOrchestrator

class ChatRequest(BaseModel):
    user_message: str
    user_id: str = "test_user" # Dummy user ID for now

app = FastAPI()

templates = Jinja2Templates(directory="src/transport_booking_agent/templates")

orchestrator = GraphOrchestrator()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(chat_request: ChatRequest):
    response = await orchestrator.handle_request(chat_request.user_message, chat_request.user_id)
    return {"response": response}