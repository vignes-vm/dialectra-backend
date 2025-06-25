class PromptManager:
    def load_template(self, filename):
        with open(f"prompts/{filename}", "r") as file:
            return file.read()

    def build_pm_prompt(self, motion):
        template = self.load_template("pm_speech.txt")
        return template.replace("{MOTION}", motion)

    def build_lo_prompt(self, motion, pm_speech):
        template = self.load_template("lo_speech.txt")
        return template.replace("{MOTION}", motion).replace("{PM_SPEECH}", pm_speech)

    def build_judge_prompt(self, motion, pm_speech, lo_speech):
        template = self.load_template("judge.txt")
        return (template
                .replace("{MOTION}", motion)
                .replace("{PM_SPEECH}", pm_speech)
                .replace("{LO_SPEECH}", lo_speech)) 