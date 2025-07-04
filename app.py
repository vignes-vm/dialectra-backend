from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from llm.llm_interface import LLMInterface
from llm.prompt_manager import PromptManager
#from firebase_admin import credentials,firestore
#import firebase_admin
from rag.debate_controller import DebateController

#cred = credentials.Certificate("firebase/firebase-admin.json")
#firebase_admin.initialize_app(cred)
from rag.judge_controller import JudgeController
from rag.vector_store import VectorStroreClient
from rag.judge_prompt import JudgePromptBuilder
vector_store=VectorStroreClient()
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
judge=JudgeController(vector_store ,llm)
@app.get("/")
def hello():
    return {"msg":llm.generate("I am the best person in the world")}


@app.post("/submit_speech/")
def submit_speech(speaker:str,context:str,motion:str):
    debate.add_speech(context,speaker,motion)
    return {"message":"Speech stored succesfully"}

@app.post("/generate_ai_response")
def generate_ai_response(motion:str,speaker_role:str,draft:str=""):
    speech=debate.generate_ai_speech(motion,speaker_role,draft)
    return {"speech":speech}

@app.post("/all_speeches/")
def all_speeches():
    docs=debate.get_all_speeches()
    return [{"speaker":d.metadata["speaker"],"context":d.page_content} for d in docs]
@app.post("/evaluate_debate/")
def evaluate_debate(motion:str):
    result=judge.evaluate_debate(motion)
    return {"judgement":result}

uvicorn.run(app, host="127.0.0.1", port=8000,reload=True)


