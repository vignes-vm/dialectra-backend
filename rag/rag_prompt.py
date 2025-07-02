class RagPromptBuilder:
    def __init__(self,retriever,llm_interface):
        self.retriever=retriever
        self.llm=llm_interface
    
    def build_prompt(self,motion,speaker_role,current_speech_draft):
        context_docs=self.retriever.retrieve_similar(current_speech_draft)
        context_text="\n\n".join([
            f"[{d.metadata.get('speaker')}]:{d.page_content}"
            for d in context_docs                          
        ])

        prompt = (
            f"You are speaking as {speaker_role} in a debate on the motion: '{motion}'.\n\n"
            f"Here are previous speeches:\n{context_text}\n\n"
            f"Based on the above, continue or respond with your speech:\n{current_speech_draft}"
        )

        return prompt

    def generate_speech(self,motion,speaker_role,speech_draft):
        full_prompt=self.build_prompt(motion,speaker_role,speech_draft)
        generated_speech= self.llm.generate(full_prompt)

        self.retriever.add_speech(speaker_role,generated_speech,metadata={"motion":motion})
        return generated_speech
    