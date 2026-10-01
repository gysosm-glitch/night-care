"""Streamlit chat UI.  Run:  streamlit run src/app.py"""
import streamlit as st

from src.agent import NightCareAgent

st.title("🌙 청주 밤샘 케어 에이전트")
st.caption("충북대생을 위한 밤·주말 병원/약국 + 이동 + 택시비 도우미 (가상 데이터)")

if "agent" not in st.session_state:
    st.session_state.agent = NightCareAgent()
    st.session_state.chat = []

for role, text in st.session_state.chat:
    st.chat_message(role).write(text)

if prompt := st.chat_input("예: 지금 밤 11시인데 열이 나. 갈 곳이랑 택시비 알려줘"):
    st.chat_message("user").write(prompt)
    agent = st.session_state.agent
    answer = agent.run(prompt)
    with st.chat_message("assistant"):
        for name, args, result in agent.tool_log:
            with st.expander(f"🔧 {name}"):
                st.code(f"{args}\n→ {result}", language="json")
        st.write(answer)
    st.session_state.chat += [("user", prompt), ("assistant", answer)]
