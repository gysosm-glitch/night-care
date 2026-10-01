# Tool Specifications

Write the spec BEFORE implementing a tool. The "Purpose" line becomes the tool description the LLM reads.

> 초안 (Claude 작성) — 팀 검토 후 이 줄을 지우세요.
> Note: tools return a SUMMARY, not every record (e.g. find_safe_spots returns only spots open now in that district).
> Valid districts everywhere: 개신동, 사창동, 복대동, 봉명동, 율량동.

## Tool: find_safe_spots
- Owner: 멤버 A
- File: src/tools/spot_tools.py
- Purpose: Find safe spots (police boxes, 24-hour convenience stores, 안심지킴이집) open at a given time in a district.
- Type: read
- Parameters: area (string, required) — district name; time (string, required) — 24-hour HH:MM
- Returns: `{"area": "봉명동", "time": "23:30", "spots": [{"id": "S11", "name": "봉명 지구대", "type": "지구대", "address": "충북 청주시 흥덕구 송절로64번길 13", "phone": "043-270-3705", "source": "공공데이터", "open_until": "24:00"}, {"id": "S7", "name": "가상 봉명 24시 편의점", "type": "24시 편의점", "source": "가상", "open_until": "24:00"}]}`
  - `address` and `phone` appear only for spots that have them (real 지구대·파출소 from 공공데이터포털). `source` is `"공공데이터"` or `"가상"`.
  - If nothing is open: `"spots": []` plus `"hint": "No safe spot open now. Call 112 in an emergency."`
- Errors: unknown area → `{"error": "Unknown area '송정동'. Valid: 개신동, 사창동, 복대동, 봉명동, 율량동."}`; bad time → `{"error": "Invalid time. Use 24-hour HH:MM, e.g. '23:10'."}`
- Example request: "봉명동 가는 길에 지금 들어갈 수 있는 안전한 곳 있어?"

## Tool: get_route
- Owner: 멤버 A
- File: src/tools/route_tools.py
- Purpose: Get the walking time, streetlight and CCTV info, and the bus option from 충북대 정문 to a district.
- Type: read
- Parameters: to (string, required) — district name; time (string, optional) — HH:MM, adds `bus_available_now`
- Returns: `{"to": "사창동", "walk_minutes": 40, "lit_ratio": 0.6, "cctv": 5, "bus_line": "가상 A1", "bus_minutes": 25, "fare": 1500, "last_bus": "22:30", "bus_available_now": false}`
  - For 개신동 (walking distance) there is no bus: `bus_line` and `last_bus` are `"-"`, `fare` is 0, `bus_available_now` is false. `bus_minutes` (5) is the car time, used for the taxi fare.
- Errors: unknown area → `{"error": "Unknown area '송정동'. Valid: 개신동, 사창동, 복대동, 봉명동, 율량동."}`; bad time → `{"error": "Invalid time. ..."}`
- Example request: "사창동까지 걸어가면 얼마나 걸리고 길은 밝아?"

## Tool: estimate_walk_risk
- Owner: 멤버 B
- File: src/tools/risk_tools.py
- Purpose: Score the risk (0-100) of walking from 충북대 정문 to a district at a given time, based on hour, streetlights, CCTV and foot traffic.
- Type: compute
- Parameters: area (string, required) — district name; time (string, required) — departure HH:MM
- Returns: `{"area": "사창동", "time": "23:10", "score": 82, "level": "높음", "reasons": ["심야 시간", "가로등 60%", "CCTV 5대", "인적 드묾", "도보 40분"]}`
- Formula (uses `data/routes.json`):
  - hour: 22:00–04:00 → +40; 20:00–22:00 or 04:00–06:00 → +20; otherwise 0
  - streetlights: `round((1 − lit_ratio) × 30)`
  - CCTV: `max(0, 10 − cctv) × 2`
  - foot traffic: +10 if time is between `busy_until` and 06:00
  - long walk: +10 if `walk_minutes` > 20
  - score is capped at 100. level: 0–29 낮음, 30–59 보통, 60+ 높음
  - check: 사창동 23:10 → 40 + 12 + 10 + 10 + 10 = **82 (높음)**; 개신동 23:10 → 40 + 3 + 0 + 0 + 0 = **43 (보통)**
- Errors: unknown area → `{"error": "Unknown area ... Valid: ..."}`; bad time → `{"error": "Invalid time. ..."}`
- Example request: "지금 밤 11시 10분인데 사창동까지 걸어가도 괜찮을까?"

## Tool: estimate_taxi_cost
- Owner: 멤버 B
- File: src/tools/taxi_tools.py
- Purpose: Estimate a taxi fare in KRW for a trip of N minutes, including the 20% night surcharge from 22:00 to 04:00.
- Type: compute
- Parameters: minutes (number, required) — trip length; time (string, required) — departure HH:MM
- Returns: `{"minutes": 25, "time": "23:10", "night": true, "fare": 9400}`
- Errors: minutes ≤ 0 → `{"error": "minutes must be positive."}`; bad time → `{"error": "Invalid time. ..."}`
- Example request: "그럼 택시 타면 얼마야?"
- Formula: `(4800 + 150 × max(0, minutes − 5)) × 1.2 if night`, rounded to 100 KRW. Use the route's `bus_minutes` as the taxi trip length.

## Tool: request_escort
- Owner: 멤버 B
- File: src/tools/escort_tools.py
- Purpose: Save a 안심귀가 escort request. Only call with confirmed=true after the user has explicitly agreed.
- Type: write
- Parameters: area (string, required) — destination district; date (string, required) — YYYY-MM-DD; time (string, required) — meeting HH:MM; meet_point (string, required) — where to meet, e.g. "충북대 정문"; confirmed (boolean, required)
- Returns: `{"saved": true, "id": "E1", "area": "사창동", "date": "2026-10-02", "time": "23:00", "meet_point": "충북대 정문"}`
- Service hours: 22:00–01:00 (from `data/escort.json`)
- Errors:
  - confirmed=false → `{"error": "User has not confirmed. Summarize the request and ask the user to confirm first."}`
  - unknown area → `{"error": "Unknown area ... Valid: ..."}`
  - outside service hours → `{"error": "Escort runs 22:00-01:00 only. Pick a time in that window or suggest a taxi."}`
  - bad date/time → `{"error": "Invalid date/time. Use YYYY-MM-DD and HH:MM."}`
- Example request: "내일 밤 11시에 정문에서 사창동까지 안심귀가 신청해 줘."

## Tool: calculate
- Owner: (given — already implemented)
- File: src/tools/calculator.py
- Purpose: Evaluate a math expression. Use this for all prices, discounts, and totals.
- Type: compute
- Parameters: expression (string, required) — e.g. "9400 - 1500"
- Returns: `{"expression": "9400 - 1500", "result": 7900}`
- Errors: invalid expression → `{"error": "Invalid expression. Use numbers and + - * / ( ) only."}`
- Example request: "택시랑 버스 요금 차이가 얼마야?"
