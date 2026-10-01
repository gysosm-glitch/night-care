# Tasks

Do ONE task at a time. Part 1 is for your team: think and write, no AI assistant, no code.

Prompt for your AI assistant (Part 2 only):
> Read AGENTS.md. Then do Task N from docs/04_tasks.md using docs/03_tool_spec.md. Only touch the files needed.

## Part 0 — Setup
- [x] **0. Copy the generic files.** Done (config, llm_client, agent, main, app, data_store).

## Part 1 — Design (no code)
- [x] **1. Brief.** `docs/01_brief.md`
- [x] **2. Data.** `data/safe_spots.json`, `routes.json`, `taxi.json`, `escort.json` (listed in `docs/02_architecture.md`)
- [x] **3. Tool map.** in `docs/03_tool_spec.md` + reskin test in `tests/scenarios.md`
- [x] **4. Tool specs.** Owner A: find_safe_spots, get_route / Owner B: estimate_walk_risk, estimate_taxi_cost, request_escort
- [x] **5. Scenarios.** `tests/scenarios.md` (A chain, B error recovery, C confirm)

## Part 2 — Build (one tool per prompt)
- [x] **6. System prompt.** `prompts/system_prompt.md`
- [x] **7. Tool 1:** `find_safe_spots` — `python -m pytest tests -k spots`
- [x] **8. Tool 2:** `get_route`
- [x] **9. Tool 3:** `estimate_walk_risk`, `estimate_taxi_cost`
- [x] **10. Tool 4:** `request_escort`
- [ ] **11. More tools (optional).**

## Part 3 — Verify
- [x] **12. Format check.** `python -m pytest tests` → all pass (no LLM needed)
- [ ] **13. Scenarios.** Run every scenario with `python -m src.main` (needs your API key). If the agent picks the wrong tool or gives up after an error, improve the tool description, the error hint, or the system prompt — not the agent code.
- [ ] **14. Demo.** See `docs/05_demo.md`.
