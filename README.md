# 🌙 청주 밤길 안심 귀가 에이전트 (Night-Care Agent)

충북대생이 밤늦게 귀가할 때 "걸어가도 괜찮은지 + 들를 수 있는 안전한 곳 + 막차/택시 + 안심귀가 신청"을 묻는 도구 호출 에이전트. (카페 에이전트와 같은 구조, 데이터는 전부 가상)

📖 **사용 설명서: [USER_GUIDE.md](USER_GUIDE.md)** (웹 앱 왼쪽 사이드바에도 사용법이 있어요)

## Setup
```
pip install -r requirements.txt
cp .env.example .env      # API_KEY 입력
python -m pytest tests    # LLM 없이 도구 + 형식 검사
python -m src.main        # CLI
python -m streamlit run streamlit_app.py  # 웹 UI
```
시나리오는 `tests/scenarios.md`, 도구 명세는 `docs/03_tool_spec.md`, 작업 순서는 `docs/04_tasks.md`, 발표 대본은 `docs/05_demo.md`.
