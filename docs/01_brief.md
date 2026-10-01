# Project Brief

한국어: [01_brief.ko.md](01_brief.ko.md)

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
- Find **real police boxes and 119 safety centers** in a district, with phone and address (공공데이터포털)
- Show the way from 충북대 정문: walking minutes, streetlight ratio, CCTV count, bus line and last bus
- **Score the walking risk (0–100)** for a district at a given time, with reasons
- Estimate a taxi fare including the 22:00–04:00 night surcharge
- **Emergency mode** (`get_emergency_guide`): steps, nearest police box, and a ready-to-send 112 text message
- **Trip home + arrival check** (`start_trip`, `check_arrival`): ETA, a message for a guardian, overdue warning
- Save a **안심귀가 escort request** (only after the user confirms; only 22:00–01:00), with a tip to verify the escort on meeting
- **Police-linked escort:** each request is linked to the real 지구대 of the destination (name, phone); the demo says clearly that nothing is actually sent to the police
- **Escort transparency** (`get_escort_info`): how escort staff are chosen (background check, training, 2-person team, photo ID) and what to check when meeting
- Calculate comparisons (e.g. bus vs taxi)
- App sidebar: one-tap 112 call/text, nearby police boxes, user guide

### v2 — planned (in priority order)
1. **Recommend, don't just report.** Every "how do I get home" answer ends with one choice (walk / bus / taxi / escort). (Prompt rule added; keep checking it.)
2. **More real facilities.** Emergency rooms and emergency bells from 공공데이터포털; map the other 13 청주 119 centers and fill 개신동's missing police box.
3. **No need to type the time.** `get_current_time` tool — the user can say "지금" instead of "23:10".
4. **More starting points.** `origin` parameter: 정문, 중문, 후문 (each with its own routes).
5. **Manage escort requests.** `list_escort_requests` and `cancel_escort` (write, confirm first).
6. **Richer risk score.** Add weekend and (fake) weather — rain lowers visibility and foot traffic.

## Out of scope
- Real APIs (경찰청, 공공데이터, bus, map), real-time GPS tracking, calling 112 or messaging friends for the user, payments, multiple users / login
- 지구대·파출소 (충북경찰청, 2026-08-03) and 119안전센터 (소방청, 2026-07-01) come from 공공데이터포털, converted once into `data/safe_spots.json`. Routes, risk inputs, fares and the escort service are fake demo data. No fake places are shown. No live API calls.
- The assistant never says a route is "100% safe" and never replaces 112.

## Why this is not a café agent (rename test)
Rename `estimate_walk_risk` → "how risky is it to walk to the latte?" and `find_safe_spots` → "which police box sells croissants?": both are nonsense for a café.
A café owner never needs "is it dark and empty at 23:30", "is a police box open nearby", "what do I text 112" (`get_emergency_guide`), or "did they get home yet?" (`check_arrival`).

## Success criteria
- **No guessing:** every time, risk score, fare, and place comes from a tool.
- **Decision:** "걸어가도 돼?" answers start with one recommendation (walk / bus / taxi / escort) and its reason.
- **Chaining:** answers that need 3 tools in a row work (risk → route → taxi).
- **Emergency:** a "따라오는 것 같아" message gets 112 + one open safe spot in the **first line**, with at most one tool call.
- **Recovery:** tool errors (unknown district, escort outside 22:00–01:00) lead to a retry or a clear question, never a crash.
- **Safe writes:** nothing is saved before the user says yes (`request_escort`, `start_trip`; v2 `cancel_escort`).
- **Short:** answers fit on one phone screen (about 5 lines or fewer, plus a list if needed).
