from llm.llm_interface import LLMInterface, LLMType
from llm.prompt_manager import PromptManager
from models.debate_state import DebateSession

class DebateOrchestrator:
    def __init__(self, llm_type=LLMType.OPENAI):
        self.llm = LLMInterface(llm_type)
        self.prompts = PromptManager()
        self.state = DebateSession()

    def run_cli(self):
        self.state.motion = self.select_motion()

        pm_prompt = self.prompts.build_pm_prompt(self.state.motion)
        self.state.pm_speech = self.llm.generate(pm_prompt)
        self.display_text("Prime Minister (Gov)", self.state.pm_speech)

        lo_prompt = self.prompts.build_lo_prompt(self.state.motion, self.state.pm_speech)
        self.state.lo_speech = self.llm.generate(lo_prompt)
        self.display_text("Leader of Opposition", self.state.lo_speech)

        judge_prompt = self.prompts.build_judge_prompt(
            self.state.motion, self.state.pm_speech, self.state.lo_speech
        )
        self.state.judgment = self.llm.generate(judge_prompt)
        self.display_text("AI Judge Verdict", self.state.judgment)

        next_action = input("\nPress [S] to save, [R] to replay, or [Q] to quit: ").lower()
        if next_action == 'r':
            self.run_cli()
        elif next_action == 's':
            from utils.file_io import save_debate
            save_debate(self.state)
            print("✅ Debate saved.")
        else:
            print("👋 Goodbye!")

    def select_motion(self):
        motions = [
            "This House would ban private education",
            "This House believes AI should not be granted copyright",
            "This House would implement a universal basic income"
        ]
        print("\n🔹 Please choose a motion for the debate:")
        for i, m in enumerate(motions, 1):
            print(f"{i}. {m}")
        print("4. [Enter your own motion]")

        choice = input("Select an option (1–4): ")
        if choice == '4':
            return input("Enter your custom motion: ")
        return motions[int(choice) - 1]

    def display_text(self, title, text):
        print(f"\n🔸 {title} Speech:\n{'-'*40}\n{text}\n{'-'*40}")
        input("\nPress [Enter] to continue...")
