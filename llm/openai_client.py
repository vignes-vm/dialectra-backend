import os
import openai
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate(self, prompt):
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a competitive debate AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
