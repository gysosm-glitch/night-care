# Architecture (same as café agent)

```
main.py (CLI) ──┐
                ├──►  agent.py  ──►  llm_client.py  ──►  LLM API (Groq / xAI)
app.py  (UI)  ──┘        │
                         └──►  tools/__init__.py (registry)  ──►  tools/*.py  ──►  data/*.json
```
Copied unchanged from the café agent: config.py, llm_client.py, agent.py (class renamed), main.py, data_store.py.
Written for this agent: docs/01_brief.md, docs/03_tool_spec.md, data/*.json, src/tools/{place,route,taxi,plan}_tools.py, prompts/system_prompt.md, tests/.

## Data files (5–10 realistic entries each is the goal; 가상 데이터)
- `data/places.json` — `{"places": [{"id","name","type","area","open","close","subjects"}]}`
- `data/routes.json` — `{"origin","routes": {"사창동": {"mode","line","minutes","fare","last_bus"}}}`
- `data/taxi.json` — fare constants (base, per minute, night window, night rate)
- `data/visit_plans.json` — `{"plans": [...]}` (written by book_visit_plan)
