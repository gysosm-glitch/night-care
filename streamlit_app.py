"""Streamlit Cloud entry point. Runs src/app.py from the repo root so `from src...` imports work."""
import os
import runpy
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

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
    "밤 11시 반에 봉명동 근처 지구대 어디 있어?",
    "지금 23:10인데 택시로 사창동 집에 갈게. 귀가 기록해 줘",
    "사창동인데 누가 따라오는 것 같아 무서워",
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


SPOT_ICONS = {"지구대": "🚓", "파출소": "🚓"}


def show_emergency() -> None:
    """Sidebar: one-tap 112 call and text buttons, always at the top."""
    st.error("🚨 **위급하면 바로 112**")
    call, text = st.columns(2)
    call.link_button("📞 112 전화", "tel:112", use_container_width=True)
    text.link_button("💬 112 문자", "sms:112", use_container_width=True)
    st.caption("말하기 어려우면 문자로 동네·큰 건물 위치를 보내세요.")


def show_safe_spots() -> None:
    """Sidebar panel: pick a district and see real police boxes open now, without asking the agent."""
    from src.tools import data_store
    from src.tools.spot_tools import find_safe_spots

    st.header("🚓 근처 지구대")
    area = st.selectbox("동네", list(data_store.load("routes")["routes"]))
    now = datetime.now(ZoneInfo("Asia/Seoul")).time().replace(second=0, microsecond=0)
    when = st.time_input("시각 (기본: 지금)", value=now, step=600)
    result = find_safe_spots(area, when.strftime("%H:%M"))
    for s in result.get("spots", []):
        line = f"{SPOT_ICONS.get(s['type'], '📍')} **{s['name']}** · {s['open_until']}까지"
        if s.get("phone"):
            line += f"  \n📞 [{s['phone']}](tel:{s['phone']}) · {s['address']}"
        st.markdown(line)
    if not result.get("spots"):
        st.info("이 동네 지구대·파출소는 공공데이터에 없어요. 다른 동네를 골라 가까운 지구대를 확인하세요.")
    st.caption("출처: 공공데이터포털 충북경찰청 지구대·파출소 현황 (2026-08-03)")
    st.divider()


with st.sidebar:
    show_emergency()
    show_safe_spots()
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
    st.caption("지구대 정보만 실제 공공데이터이고, 길·위험도·요금·안심귀가는 수업용 가상 데이터예요.")

runpy.run_path(str(Path(__file__).parent / "src" / "app.py"), run_name="__main__")
