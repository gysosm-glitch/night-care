"""Streamlit Cloud entry point. Runs src/app.py from the repo root so `from src...` imports work."""
import os
import runpy
from pathlib import Path

import streamlit as st

# Open the guide sidebar by default so first-time users see how to use the app.
st.set_page_config(page_title="밤길 지킴이", page_icon="🌙", initial_sidebar_state="expanded")

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

GUIDE_PATH = Path(__file__).parent / "USER_GUIDE.md"


def guide_sections() -> list:
    """Split USER_GUIDE.md into (title, body) pairs, one per '## ' heading."""
    try:
        text = GUIDE_PATH.read_text(encoding="utf-8")
    except OSError:
        return []
    sections = []
    for block in text.split("\n## ")[1:]:
        title, _, body = block.partition("\n")
        sections.append((title.strip(), body.replace("\n---", "").strip()))
    return sections


with st.sidebar:
    st.header("📖 사용 설명서")
    st.caption("궁금한 항목을 눌러 펼쳐 보세요.")
    for i, (title, body) in enumerate(guide_sections()):
        with st.expander(title, expanded=(i == 0)):
            st.markdown(body)
    st.subheader("💬 예시 질문")
    st.caption("오른쪽 위 복사 버튼을 눌러 아래 입력창에 붙여 넣으세요.")
    for example in EXAMPLES:
        st.code(example, language=None, wrap_lines=True)
    if st.button("🔄 대화 새로 시작", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    st.warning("모든 정보는 데모용 **가상 데이터**예요. 위급하면 바로 **112**에 신고하세요.")

runpy.run_path(str(Path(__file__).parent / "src" / "app.py"), run_name="__main__")
