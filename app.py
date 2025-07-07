from fastapi import FastAPI, Body, Path, Query, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.language_models import LLM
import uvicorn
from pydantic import BaseModel
from starlette.websockets import WebSocket

from llm.llm_interface import LLMInterface
from llm.prompt_manager import PromptManager
from firebase_admin import credentials
import firebase_admin
from rag.debate_controller import DebateController
from asian_parlimentary.service.asian_parilamentry_service import AsianParliamentaryService
from websocket.websocket_manager import manager


cred = credentials.Certificate("firebase/firebase-admin.json")
firebase_admin.initialize_app(cred, name="debate_app")

class CreateSession(BaseModel):
    topic:str

debate=DebateController()

app = FastAPI(
    title="Debate API", 
    description="API for AI-Powered 1v1 Debate Simulator",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize with default LLM type (OpenAI)
llm = LLMInterface()
prompts = PromptManager()

@app.get("/")
def hello():
    return {"msg":llm.generate("I am the best person in the world")}

@app.post("/create_session")
def create_session(topic:CreateSession):
    asian_parliamentary_service = AsianParliamentaryService(topic.topic)
    session_id = asian_parliamentary_service.create_session()
    return {"id": session_id, "message": "Debate session created successfully"}


@app.post("/submit_speech")
def submit_speech(speaker:str,context:str):
    debate.add_speech(context,speaker)
    return {"message":"Speech stored succesfully"}

@app.post("/generate_ai_respons")
def generate_ai_response(motion:str,speaker_role:str,draft:str=""):
    speech=debate.generate_ai_speech(motion,speaker_role,draft)
    return {"speech":speech}

@app.post("/all_speeches/")
def all_speeches():
    docs=debate.get_all_speeches()
    return [{"speaker":d.metadata["speaker"],"context":d.page_context} for d in docs]

@app.get("/debate/{session_id}")
def get_debate_session(session_id: str = Path(...)):
    """
    Get information about a specific debate session.

    Args:
        session_id: The ID of the debate session

    Returns:
        The debate session information
    """
    asian_parliamentary_service = AsianParliamentaryService("")
    debate_session = asian_parliamentary_service.get_session(session_id)
    if not debate_session:
        return {"error": "Debate session not found"}

    # Add the number of connected clients to the response
    connections = manager.get_connections(session_id)
    debate_session["connected_clients"] = len(connections)

    return debate_session

@app.websocket("/debate/{session_id}/ws")
async def websocket_endpoint(websocket: WebSocket, session_id: str = Path(...)):
    """
    WebSocket endpoint for a specific debate session.

    Args:
        websocket: The WebSocket connection
        session_id: The ID of the debate session
    """
    try:
        # Connect to the specific debate session
        await manager.connect(websocket, session_id)

        # Get the current debate session
        asian_parliamentary_service = AsianParliamentaryService("")
        debate_session:dict = asian_parliamentary_service.get_session(session_id)
        await manager.send_message(
          debate_session,
            session_id,
            websocket
        )
        # asian_parliamentary_service.add_speech(session_id, "PM", "This is the first speech of the debate.")
        while True:
            speakers:list = debate_session.get("speakers")
            current_speaker_index = debate_session.get("current_speaker_index")
            content = LLMInterface().generate(speakers[current_speaker_index].get("prompt"))
            await manager.send_message(
                content,
                session_id,
                websocket
            )
            debate_session["current_speaker_index"] = (debate_session["current_speaker_index"] + 1) % len(debate_session["speakers"])
            asian_parliamentary_service.update_session(session_id, debate_session)

    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)



uvicorn.run(app, host="127.0.0.1", port=8000)
