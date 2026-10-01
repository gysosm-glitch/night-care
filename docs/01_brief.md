# Project Brief

> 초안 (Claude 작성) — 팀 검토 후 이 줄을 지우세요.

## Goal
Help a 충북대 student **decide how to get home safely at night — walk, bus, taxi, or escort — and stay with them until they arrive.**
The assistant does not just list facts. It uses **tools** to gather them (risk, route, last bus, fare, open safe spots) and ends every answer with **one clear recommendation and the reason**.

## Users and situations
A 충북대 student living alone near campus (개신동/사창동/복대동/봉명동/율량동). Not technical, often tired or anxious, reading on a phone. Three situations matter:

| Situation | What they need | Answer style |
|---|---|---|
| **Before leaving** — "알바 끝났어, 사창동까지 걸어가도 돼?" | A decision: walk / bus / taxi / escort | Recommendation first, then 2–3 facts |
| **On the way, uneasy** — "누가 따라오는 것 같아" | The nearest open safe spot, right now | 112 first, one place, no analysis |
| **Planning ahead** — "내일 밤 11시 안심귀가 신청해 줘" | Book / check / cancel an escort | Confirm before any change |

## What the assistant can do
### v1 — built
- Find **safe spots open right now** in a district (지구대·파출소, 24시 편의점, 안심지킴이집)
- Show the way from 충북대 정문: walking minutes, streetlight ratio, CCTV count, bus line and last bus
- **Score the walking risk (0–100)** for a district at a given time, with reasons
- Estimate a taxi fare including the 22:00–04:00 night surcharge
- Save a **안심귀가 escort request** (only after the user confirms; only 22:00–01:00)
- Calculate comparisons (e.g. bus vs taxi)

### v2 — planned (in priority order)
1. **Recommend, don't just report.** System prompt rule: every "how do I get home" answer ends with one choice (walk / bus / taxi / escort) based on risk level and `bus_available_now`.
2. **Emergency mode.** If the user says they feel followed, threatened, or scared, skip the risk analysis: tell them to call 112 and give the single nearest open safe spot (`find_safe_spots`).
3. **No need to type the time.** `get_current_time` tool — the user can say "지금" instead of "23:10".
4. **Safe-arrival check-in.** `start_trip` saves "leaving now, expected arrival HH:MM" (write, confirm first); `check_arrival` marks the trip done or, if overdue, suggests contacting a friend or 112.
5. **More starting points.** `origin` parameter: 정문, 중문, 후문 (each with its own routes).
6. **Manage escort requests.** `list_escort_requests` and `cancel_escort` (write, confirm first).
7. **Richer risk score.** Add weekend and (fake) weather — rain lowers visibility and foot traffic.

## Out of scope
- Real APIs (경찰청, 공공데이터, bus, map), real-time GPS tracking, calling 112 or messaging friends for the user, payments, multiple users / login
- ALL data is fake demo data in `data/*.json`
- The assistant never says a route is "100% safe" and never replaces 112.

## Why this is not a café agent (rename test)
Rename `estimate_walk_risk` → "how risky is it to walk to the latte?" and `find_safe_spots` → "which police box sells croissants?": both are nonsense for a café.
A café owner never needs "is it dark and empty at 23:30", "is a police box open nearby", "book someone to walk me home", or "did she get home yet?" (`check_arrival`).

## Success criteria
- **No guessing:** every time, risk score, fare, and place comes from a tool.
- **Decision:** "걸어가도 돼?" answers start with one recommendation (walk / bus / taxi / escort) and its reason.
- **Chaining:** answers that need 3 tools in a row work (risk → route → taxi).
- **Emergency:** a "따라오는 것 같아" message gets 112 + one open safe spot in the **first line**, with at most one tool call.
- **Recovery:** tool errors (unknown district, escort outside 22:00–01:00) lead to a retry or a clear question, never a crash.
- **Safe writes:** nothing is saved before the user says yes (`request_escort`, v2 `start_trip`, `cancel_escort`).
- **Short:** answers fit on one phone screen (about 5 lines or fewer, plus a list if needed).
