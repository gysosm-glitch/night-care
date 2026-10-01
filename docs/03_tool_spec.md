# Tool Specifications

Write the spec BEFORE implementing a tool. The "Purpose" line becomes the tool description the LLM reads.

> 초안 (Claude 작성) — 팀 검토 후 이 줄을 지우세요.
> Note: tools return a SUMMARY, not every record (e.g. find_safe_spots returns only spots open now in that district).
> Valid districts everywhere: 개신동, 사창동, 복대동, 봉명동, 율량동.

## Tool: find_safe_spots
- Owner: 멤버 A
- File: src/tools/spot_tools.py
- Purpose: Find real public safety places (police boxes and other facilities) open at a given time in a district, with phone and address.
- Type: read
- Parameters: area (string, required) — district name; time (string, required) — 24-hour HH:MM
- Returns: `{"area": "봉명동", "time": "23:30", "spots": [{"id": "S11", "name": "봉명 지구대", "type": "지구대", "address": "충북 청주시 흥덕구 송절로64번길 13", "phone": "043-270-3705", "source": "공공데이터", "open_until": "24:00"}]}`
  - Only real data from 공공데이터포털 (no fake places): 지구대·파출소 and 119안전센터 (`type`). 개신동 currently has none.
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
- Returns: `{"saved": true, "id": "E1", "area": "사창동", "date": "2026-10-02", "time": "23:00", "meet_point": "충북대 정문", "police": {"name": "사창 지구대", "phone": "043-251-1703", "address": "충북 청주시 서원구 1순환로 690"}, "police_note": "실제 서비스라면 신청 내용이 관할 지구대에 공유됩니다. (데모라 실제로 전달되지 않음)", "verify": "만나면 요원이 먼저 신청 번호 E1을 말하는지 확인하고, 요원의 사진 신분증(얼굴·이름)을 보여 달라고 하세요. 2인 1조가 아니거나 의심되면 따라가지 말고 112 또는 관할 사창 지구대(043-251-1703)에 연락하세요. 실제 서비스라면 신청 내용이 관할 지구대에 공유됩니다. (데모라 실제로 전달되지 않음)"}`
  - **Police link:** `police` is the real 지구대·파출소 of the destination district (from `data/safe_spots.json`); its id is saved with the request as `police_id`. If the district has none in the data (개신동), `police` is null and `police_note` says to use 112.
- Service hours: 22:00–01:00 (from `data/escort.json`)
- Errors:
  - confirmed=false → `{"error": "User has not confirmed. Summarize the request and ask the user to confirm first."}`
  - unknown area → `{"error": "Unknown area ... Valid: ..."}`
  - outside service hours → `{"error": "Escort runs 22:00-01:00 only. Pick a time in that window or suggest a taxi."}`
  - bad date/time → `{"error": "Invalid date/time. Use YYYY-MM-DD and HH:MM."}`
- Example request: "내일 밤 11시에 정문에서 사창동까지 안심귀가 신청해 줘."

## Tool: get_escort_info
- Owner: 멤버 B
- File: src/tools/escort_tools.py
- Purpose: Get how 안심귀가 escort staff are chosen and how to check the escort's identity when you meet.
- Type: read
- Parameters: (none)
- Returns: `{"note": "데모 서비스 기준(예시)", "hours": "22:00-01:00", "staff_criteria": ["성범죄·강력범죄 경력 조회를 통과한 사람만 선발", ...], "check_on_meet": ["요원이 먼저 신청 번호(예: E1)를 말하는지 확인", ...]}`
  - From `data/escort.json` → `service`. The service is demo data, so `note` says these are example rules.
- Errors: none expected (reads a local file).
- Example request: "안심귀가 하면 어떤 사람이 와? 믿을 수 있어?"

## Tool: get_emergency_guide
- Owner: 멤버 A
- File: src/tools/emergency_tools.py
- Purpose: Get what to do right now in an emergency: short steps, open safe places in the district, and a ready-to-send 112 text message.
- Type: read
- Parameters: area (string, required) — district the user is in or near; time (string, required) — HH:MM; situation (string, optional) — short description, default "누군가 따라오는 것 같아요"
- Returns: `{"call": "112", "steps": ["밝고 사람 많은 큰길·가게로 이동하세요.", "112에 전화하세요. 말하기 어려우면 112로 문자 신고하세요.", "아래 지구대가 가까우면 들어가세요."], "spots": [{"name": "사창 지구대", "phone": "043-251-1703", "address": "..."}], "sms_112": "[긴급] 청주시 사창동 부근, 23:30. 누군가 따라오는 것 같아요. 도와주세요."}`
  - `spots`: at most 2, from find_safe_spots. Empty list if none.
- Errors: unknown area → `{"error": "Unknown area ... Call 112 now and say where you are."}`; bad time → `{"error": "Invalid time. ..."}`
- Example request: "사창동인데 누가 따라오는 것 같아 무서워"

## Tool: start_trip
- Owner: 멤버 B
- File: src/tools/trip_tools.py
- Purpose: Save a trip home from 충북대 정문 and compute the expected arrival time and a message for a guardian. Only call with confirmed=true after the user has explicitly agreed.
- Type: write
- Parameters: area (string, required) — destination district; time (string, required) — departure HH:MM; mode (string, required) — 도보, 버스, or 택시; confirmed (boolean, required)
- Returns: `{"saved": true, "id": "T1", "area": "사창동", "mode": "택시", "depart": "23:10", "eta": "23:35", "guardian_message": "나 23:10에 충북대 정문에서 출발해서 사창동으로 택시 타고 가는 중이야. 23:35쯤 도착 예정. 23:45까지 연락 없으면 전화해 줘!"}`
- Minutes: 도보 → `walk_minutes`, 버스·택시 → `bus_minutes` (from `data/routes.json`). ETA wraps past midnight.
- Errors:
  - confirmed=false → `{"error": "User has not confirmed. Summarize the trip and ask the user to confirm first."}`
  - unknown area / bad time → same hints as get_route
  - bad mode → `{"error": "Unknown mode '자전거'. Use 도보, 버스, or 택시."}`
  - bus after last bus or no bus line → `{"error": "No bus to 사창동 now (last bus 22:30). Use 도보 or 택시."}`
- Example request: "지금 23:10인데 택시로 사창동 출발할게. 기록해 줘"

## Tool: check_arrival
- Owner: 멤버 B
- File: src/tools/trip_tools.py
- Purpose: Mark a saved trip as arrived, or check whether it is overdue and what to do.
- Type: write
- Parameters: trip_id (string, required) — e.g. "T1"; time (string, required) — current HH:MM; arrived (boolean, required) — true if the user says they got home
- Returns:
  - arrived → `{"id": "T1", "status": "arrived"}` (saved)
  - not yet, on time → `{"id": "T1", "status": "on_the_way", "eta": "23:35", "minutes_left": 10}`
  - not yet, more than 10 minutes late → `{"id": "T1", "status": "overdue", "eta": "23:35", "minutes_late": 15, "advice": "Ask if they are safe. Suggest contacting their guardian; if in danger, call 112."}`
- Errors: unknown trip → `{"error": "Unknown trip 'T9'. Call start_trip first or check the trip id."}`; bad time → `{"error": "Invalid time. ..."}`
- No separate confirmation: the user saying "도착했어" is the confirmation.
- Example request: "나 도착했어" / "아직 가는 중인데 늦어지고 있어"

## Tool: calculate
- Owner: (given — already implemented)
- File: src/tools/calculator.py
- Purpose: Evaluate a math expression. Use this for all prices, discounts, and totals.
- Type: compute
- Parameters: expression (string, required) — e.g. "9400 - 1500"
- Returns: `{"expression": "9400 - 1500", "result": 7900}`
- Errors: invalid expression → `{"error": "Invalid expression. Use numbers and + - * / ( ) only."}`
- Example request: "택시랑 버스 요금 차이가 얼마야?"
