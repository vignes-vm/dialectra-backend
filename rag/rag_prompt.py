class RagPromptBuilder:
    def __init__(self,retriever,llm_interface):
        self.retriever=retriever
        self.llm=llm_interface
    
    def build_prompt(self, motion, speaker_role, current_speech_draft):
        context_docs = self.retriever.retrieve_similar(current_speech_draft)
        context_text = "\n\n".join([
            f"[{d.metadata.get('speaker', 'Unknown Speaker')}]: {d.page_content}"
            for d in context_docs
        ])

        prompt = (
            f"You are speaking as {speaker_role} in a formal debate on the motion: '{motion}'.\n\n"
            f"Here are previous speeches:\n{context_text}\n\n"
            f"Now deliver your speech. Keep it concise, no longer than 150 words.\n"
            f"Ensure your speech is highly relevant to the previous arguments and reflects your speaker role.\n\n"
            f"Start your speech:\n{current_speech_draft.strip()}"
        )
        return prompt


    def generate_speech(self,motion,speaker_role,speech_draft):
        full_prompt=self.build_prompt(motion,speaker_role,speech_draft)
        generated_speech= self.llm.generate(full_prompt)

        self.retriever.add_speech(speaker_role,generated_speech,metadata={"motion":motion})
        return generated_speech
    