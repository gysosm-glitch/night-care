"""Streamlit chat UI.  Run:  streamlit run src/app.py"""
import streamlit as st

from src.agent import NightCareAgent

st.title("🌙 청주 밤길 안심 귀가 에이전트")
st.caption("충북대생을 위한 밤길 위험도 · 근처 지구대 · 막차/택시 · 귀가 기록 · 위급 안내 도우미")

if "agent" not in st.session_state:
    st.session_state.agent = NightCareAgent()
    st.session_state.chat = []

for role, text in st.session_state.chat:
    st.chat_message(role).write(text)

if prompt := st.chat_input("예: 지금 밤 11시 10분인데 사창동까지 걸어가도 괜찮을까?"):
    st.chat_message("user").write(prompt)
    agent = st.session_state.agent
    answer = agent.run(prompt)
    with st.chat_message("assistant"):
        for name, args, result in agent.tool_log:
            with st.expander(f"🔧 {name}"):
                st.code(f"{args}\n→ {result}", language="json")
        st.write(answer)
    st.session_state.chat += [("user", prompt), ("assistant", answer)]
