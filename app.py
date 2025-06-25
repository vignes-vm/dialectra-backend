import streamlit as st
from llm.openai_client import LLMClient
from llm.prompt_manager import PromptManager
from models.debate_state import DebateSession

llm = LLMClient()
prompts = PromptManager()
state = DebateSession()

st.set_page_config(page_title="1v1 Debate Simulator", layout="centered")
st.title("🧠 AI-Powered 1v1 Debate Simulator")

st.header("Step 1: Select or Enter a Motion")
default_motions = [
    "This House would ban private education",
    "This House believes AI should not be granted copyright",
    "This House would implement a universal basic income"
]

motion_option = st.radio("Choose a motion:", default_motions + ["Enter your own"], index=0)
if motion_option == "Enter your own":
    state.motion = st.text_input("Your Motion:")
else:
    state.motion = motion_option

if state.motion:
    if st.button("🗣️ Generate Prime Minister Speech"):
        pm_prompt = prompts.build_pm_prompt(state.motion)
        state.pm_speech = llm.generate(pm_prompt)
        st.session_state["pm_speech"] = state.pm_speech

    if "pm_speech" in st.session_state:
        st.subheader("🧑‍⚖️ Prime Minister (Gov) Speech")
        st.markdown(st.session_state["pm_speech"])

    if "pm_speech" in st.session_state and st.button("🗣️ Generate Leader of Opposition Speech"):
        lo_prompt = prompts.build_lo_prompt(state.motion, st.session_state["pm_speech"])
        state.lo_speech = llm.generate(lo_prompt)
        st.session_state["lo_speech"] = state.lo_speech

    if "lo_speech" in st.session_state:
        st.subheader("🧑‍⚖️ Leader of Opposition Speech")
        st.markdown(st.session_state["lo_speech"])

    if "lo_speech" in st.session_state and st.button("⚖️ Get AI Judge Verdict"):
        judge_prompt = prompts.build_judge_prompt(
            state.motion,
            st.session_state["pm_speech"],
            st.session_state["lo_speech"]
        )
        state.judgment = llm.generate(judge_prompt)
        st.session_state["judgment"] = state.judgment

    if "judgment" in st.session_state:
        st.subheader("🏆 AI Judge Verdict")
        st.markdown(st.session_state["judgment"])

    if "judgment" in st.session_state and st.button("💾 Save Debate to File"):
        from utils.file_io import save_debate
        state.pm_speech = st.session_state["pm_speech"]
        state.lo_speech = st.session_state["lo_speech"]
        state.judgment = st.session_state["judgment"]
        save_debate(state)
        st.success("Debate session saved!")
else:
    st.info("Please enter or select a motion to begin.")
