# Architecture (same as café agent)

```
main.py (CLI) ──┐
                ├──►  agent.py  ──►  llm_client.py  ──►  LLM API (Groq / xAI)
app.py  (UI)  ──┘        │
                         └──►  tools/__init__.py (registry)  ──►  tools/*.py  ──►  data/*.json
```
Copied unchanged from the café agent: config.py, llm_client.py, agent.py (class renamed), main.py, data_store.py.
Written for this agent: docs/01_brief.md, docs/03_tool_spec.md, data/*.json, src/tools/{spot,route,risk,taxi,escort,emergency,trip}_tools.py, prompts/system_prompt.md, tests/.

## Data files (5–10 realistic entries each is the goal; 가상 데이터)
> 초안 (Claude 작성) — 팀 검토 후 이 줄을 지우세요.

- `data/safe_spots.json` — `{"source_note", "spots": [{"id","name","type","area","open","close","source", "address"?, "phone"?}]}`
  - 지구대·파출소 (`source: "공공데이터"`): converted from `data/경찰청 충청북도경찰청_지구대 파출소 현황_20260803.csv` (공공데이터포털, cp949). Matched to a district by station name (사창·복대·봉명·율량). The file has no 서원경찰서 stations, so 개신동 has none.
  - 119안전센터 (`source: "공공데이터"`): from `data/소방청_119안전센터 현황_20260701.zip` (CSV inside, cp949). Of 14 청주 centers only 복대119안전센터 matches a district by name; the others are not mapped yet.
  - Only real data (fake stores and 안심지킴이집 were removed). type: 지구대, 파출소, 119안전센터
- `data/routes.json` — `{"origin": "충북대 정문", "routes": {"사창동": {"walk_minutes","lit_ratio","cctv","busy_until","bus_line","bus_minutes","fare","last_bus"}}}`
  - lit_ratio: 0.0–1.0, share of the walking route with streetlights
  - cctv: number of CCTVs on the walking route
  - busy_until: HH:MM after which the street is quiet (shops closed, few people)
- `data/taxi.json` — fare constants (base, per minute, night window, night rate) — unchanged
- `data/trips.json` — `{"trips": [{"id","area","mode","depart","eta","status"}]}` (written by start_trip / check_arrival; status: on_the_way, arrived)
- `data/escort.json` — `{"service": {"start": "22:00", "end": "01:00"}, "requests": [...]}` (requests written by request_escort)

Removed from the old night-care version: `data/places.json` (clinics/pharmacies), `data/visit_plans.json`.
