from llm.openai_client import LLMClient as OpenAIClient
from llm.llm_client_langchain import LLMClientLangChain
from enum import Enum

class LLMType(Enum):
    OPENAI = "openai"
    LANGCHAIN_GEMINI = "langchain_gemini"

class LLMInterface:
    def __init__(self, llm_type=LLMType.LANGCHAIN_GEMINI):
        self.llm_type = llm_type
        if llm_type == LLMType.OPENAI:
            self.client = OpenAIClient()
        elif llm_type == LLMType.LANGCHAIN_GEMINI:
            self.client = LLMClientLangChain()
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")

    def generate(self, prompt):
        return self.client.generate(prompt)
    
    def set_llm_type(self, llm_type):
        if llm_type != self.llm_type:
            self.llm_type = llm_type
            if llm_type == LLMType.OPENAI:
                self.client = OpenAIClient()
            elif llm_type == LLMType.LANGCHAIN_GEMINI:
                self.client = LLMClientLangChain()
            else:
                raise ValueError(f"Unsupported LLM type: {llm_type}")