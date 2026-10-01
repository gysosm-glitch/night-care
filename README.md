# 🌙 청주 밤샘 케어 에이전트 (Night-Care Agent)

충북대생이 밤·주말에 아플 때 "지금 갈 수 있는 곳 + 가는 법 + 비용"을 묻는 도구 호출 에이전트. (카페 에이전트와 같은 구조, 데이터는 전부 가상)

## Setup
```
pip install -r requirements.txt
cp .env.example .env      # API_KEY 입력
python -m pytest tests    # LLM 없이 도구 + 형식 검사
python -m src.main        # CLI
streamlit run src/app.py  # 웹 UI
```
시나리오는 `tests/scenarios.md`, 도구 명세는 `docs/03_tool_spec.md`, 작업 순서는 `docs/04_tasks.md`, 발표 대본은 `docs/05_demo.md`.
