from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from llm.llm_interface import LLMInterface
from llm.prompt_manager import PromptManager


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

uvicorn.run(app, host="0.0.0.0", port=8000)