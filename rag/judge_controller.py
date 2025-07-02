from rag.judge_prompt import JudgePromptBuilder
class JudgeController:
    def __init__(self,vectorstore,llm_interface):
        self.vectorstore=vectorstore
        self.prompt_builder=JudgePromptBuilder()
        self.llm=llm_interface
    
    def evaluate_debate(self,motion):
        docs=self.vectorstore.get_all_documents()
        prompt=self.prompt_builder.build_prompt(motion,docs)
        response=self.llm.generate(prompt)
        return response