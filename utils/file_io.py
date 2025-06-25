import os
import datetime

def save_debate(state):
    folder = "debate_logs"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{folder}/debate_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Motion: {state.motion}\n\n")
        f.write("=== Prime Minister ===\n")
        f.write(state.pm_speech + "\n\n")
        f.write("=== Leader of Opposition ===\n")
        f.write(state.lo_speech + "\n\n")
        f.write("=== Judge Verdict ===\n")
        f.write(state.judgment)