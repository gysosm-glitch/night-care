"""Streamlit Cloud entry point. Runs src/app.py from the repo root so `from src...` imports work."""
import os
import runpy
from pathlib import Path

import streamlit as st

# Streamlit Cloud keeps keys in st.secrets; config.py reads env vars, so copy them over.
try:
    for key, value in st.secrets.items():
        if isinstance(value, str):
            os.environ.setdefault(key, value)
except Exception:
    pass  # no secrets.toml (local run) -> config.py falls back to .env

EXAMPLES = [
    "지금 밤 11시 10분인데 사창동까지 걸어가도 괜찮을까?",
    "밤 11시 반에 봉명동 가는데 들를 수 있는 안전한 곳 있어?",
    "밤 11시에 사창동 가는 택시비랑 버스비 차이 알려줘",
    "내일 밤 11시에 충북대 정문에서 사창동까지 안심귀가 신청해 줘",
]

with st.sidebar:
    st.header("📖 사용 방법")
    st.markdown(
        "1. **지금 시각**과 **가려는 동네**를 함께 적어 주세요.\n"
        "2. 답변 위의 🔧 를 누르면 에이전트가 어떤 도구로 확인했는지 볼 수 있어요.\n"
        "3. 안심귀가 신청은 내용을 확인한 뒤 **\"응\"** 이라고 답해야 저장돼요."
    )
    st.subheader("📍 지원 지역 (충북대 정문 출발)")
    st.markdown("개신동 · 사창동 · 복대동 · 봉명동 · 율량동")
    st.subheader("💬 예시 질문")
    st.caption("오른쪽 위 복사 버튼을 눌러 아래 입력창에 붙여 넣으세요.")
    for example in EXAMPLES:
        st.code(example, language=None)
    st.subheader("❓ 이런 걸 알려줘요")
    st.markdown(
        "- 걸어가도 괜찮은지 (위험도 0~100점)\n"
        "- 지금 열린 지구대·24시 편의점·안심지킴이집\n"
        "- 도보 시간, 가로등·CCTV, 막차 시간\n"
        "- 심야 할증 포함 택시비\n"
        "- 안심귀가 동행 신청 (22:00~01:00)"
    )
    if st.button("🔄 대화 새로 시작", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    st.warning("모든 정보는 데모용 **가상 데이터**예요. 위급하면 바로 **112**에 신고하세요.")

runpy.run_path(str(Path(__file__).parent / "src" / "app.py"), run_name="__main__")
