from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

class LLMClientLangChain:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),  
            convert_system_message_to_human=True,
            temperature=0.65
        )

    def generate(self, prompt):
        system_template = "you are a competitive debate AI."
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("user", "{prompt}")
        ])
        messages  = chat_prompt.invoke({"prompt": prompt})
        response = self.model.invoke(messages)
        return response.content
