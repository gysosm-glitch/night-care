# Architecture (same as café agent)

```
main.py (CLI) ──┐
                ├──►  agent.py  ──►  llm_client.py  ──►  LLM API (Groq / xAI)
app.py  (UI)  ──┘        │
                         └──►  tools/__init__.py (registry)  ──►  tools/*.py  ──►  data/*.json
```
Copied unchanged from the café agent: config.py, llm_client.py, agent.py (class renamed), main.py, data_store.py.
Written for this agent: docs/01_brief.md, docs/03_tool_spec.md, data/*.json, src/tools/{spot,route,risk,taxi,escort}_tools.py, prompts/system_prompt.md, tests/.

## Data files (5–10 realistic entries each is the goal; 가상 데이터)
> 초안 (Claude 작성) — 팀 검토 후 이 줄을 지우세요.

- `data/safe_spots.json` — `{"spots": [{"id","name","type","area","open","close"}]}`
  - type: 지구대, 파출소, 24시 편의점, 안심지킴이집
- `data/routes.json` — `{"origin": "충북대 정문", "routes": {"사창동": {"walk_minutes","lit_ratio","cctv","busy_until","bus_line","bus_minutes","fare","last_bus"}}}`
  - lit_ratio: 0.0–1.0, share of the walking route with streetlights
  - cctv: number of CCTVs on the walking route
  - busy_until: HH:MM after which the street is quiet (shops closed, few people)
- `data/taxi.json` — fare constants (base, per minute, night window, night rate) — unchanged
- `data/escort.json` — `{"service": {"start": "22:00", "end": "01:00"}, "requests": [...]}` (requests written by request_escort)

Removed from the old night-care version: `data/places.json` (clinics/pharmacies), `data/visit_plans.json`.
