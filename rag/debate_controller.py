from rag.rag_prompt import RagPromptBuilder
from rag.vector_store import VectorStroreClient
from llm.llm_interface import LLMInterface

class DebateController:
    def __init__(self):
        self.vectorstore=VectorStroreClient()
        self.llm_interface=LLMInterface()
        self.rag=RagPromptBuilder(self.vectorstore,self.llm_interface)
    
    def add_speech(self,context,speaker):
        self.vectorstore.add_speech(speaker,context)

    def generate_ai_speech(self,motion,speaker_role,draft=""):
        return self.rag.generate_speech(motion,speaker_role,draft)
    
    def get_all_speeches(self):
        return self.vectorstore.get_all_documents()