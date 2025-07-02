class JudgePromptBuilder:
    def __init__(self):
        pass
    def build_prompt(self,motion,speech_docs):
        speech_texts="\n\n".join([f"[{doc.metadata.get('speaker')}]:{doc.page_content}"
        for doc in speech_docs
        ])

        prompt=(
            f"You are an impartial debate adjudicator.\n\n"
            f"**Motion:** \"{motion}\"\n\n"
            f"**Debate Speeches:**\n{speech_texts}\n\n"
            f"Evaluate each speaker on the following criteria (0–10):\n"
            f"- Clarity\n"
            f"- Relevance to the motion\n"
            f"- Persuasiveness\n\n"
            f"Then declare:\n"
            f"- Which team won the debate (Government or Opposition)\n"
            f"- Give a clear justification for your decision.\n\n"
            f"Respond in JSON format like this:\n\n"
            f"{{\n"
            f"  \"scores\": {{\n"
            f"    \"Speaker Name\": {{\"clarity\": x, \"relevance\": y, \"persuasiveness\": z}},\n"
            f"    ...\n"
            f"  }},\n"
            f"  \"winner\": \"Government\" or \"Opposition\",\n"
            f"  \"feedback\": \"Detailed explanation\"\n"
            f"}}"
        )
        return prompt
