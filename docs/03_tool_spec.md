# Tool Specifications

Write the spec BEFORE implementing a tool. The "Purpose" line becomes the tool description the LLM reads.

> Note: tools return a SUMMARY, not every record (e.g. find_open_places returns only places open now).

## Tool: find_open_places
- Owner: 멤버 A
- File: src/tools/place_tools.py
- Purpose: Find clinics and pharmacies open at a given time for a given medical subject.
- Type: read
- Parameters: time (string, required) — 24-hour HH:MM; subject (string, required) — 내과, 소아과, 정형외과, 외과, 이비인후과, 일반의약품, 상비약
- Returns: `{"time": "23:10", "subject": "내과", "places": [{"id": "C1", "name": "가상 24시 응급의료센터", "type": "응급실", "area": "사창동", "open_until": "24:00"}]}`
- Errors: unknown subject → `{"error": "No place for '치과'. Valid subjects: ..."}`; bad time → `{"error": "Invalid time. Use 24-hour HH:MM, e.g. '23:10'."}`
- Example request: "밤 11시에 열린 내과 있어?"

## Tool: get_route
- Owner: 멤버 A
- File: src/tools/route_tools.py
- Purpose: Get the travel mode, minutes, fare and last bus from 충북대 정문 to a district.
- Type: read
- Parameters: to (string, required) — 사창동, 복대동, 개신동, 율량동; time (string, optional) — HH:MM, adds `bus_available_now`
- Returns: `{"to": "사창동", "mode": "버스", "line": "가상 A1", "minutes": 25, "fare": 1500, "last_bus": "22:30", "bus_available_now": false}`
- Errors: unknown area → `{"error": "Unknown area '송정동'. Valid: 사창동, 복대동, 개신동, 율량동."}`
- Example request: "사창동까지 버스 아직 있어?"

## Tool: estimate_taxi_cost
- Owner: 멤버 B
- File: src/tools/taxi_tools.py
- Purpose: Estimate a taxi fare in KRW for a trip of N minutes, including the 20% night surcharge from 22:00 to 04:00.
- Type: compute
- Parameters: minutes (number, required) — trip length; time (string, required) — departure HH:MM
- Returns: `{"minutes": 12, "time": "23:10", "night": true, "fare": 7000}`
- Errors: minutes ≤ 0 → `{"error": "minutes must be positive."}`; bad time → `{"error": "Invalid time. ..."}`
- Example request: "그럼 택시 타면 얼마야?"
- Formula: `(4800 + 150 × max(0, minutes − 5)) × 1.2 if night`, rounded to 100 KRW.

## Tool: book_visit_plan
- Owner: 멤버 B
- File: src/tools/plan_tools.py
- Purpose: Save a clinic visit plan. Only call with confirmed=true after the user has explicitly agreed.
- Type: write
- Parameters: clinic_id (string, required); date (string, required) — YYYY-MM-DD; time (string, required) — HH:MM; note (string, required); confirmed (boolean, required)
- Returns: `{"saved": true, "id": "P1", "clinic": "가상 충대앞 이비인후과", "date": "2026-10-02", "time": "10:00"}`
- Errors:
  - confirmed=false → `{"error": "User has not confirmed. Ask the user to confirm first, ..."}`
  - unknown clinic → `{"error": "Unknown clinic 'X9'. Call find_open_places to get valid ids."}`
  - clinic closed at that time → `{"error": "... is closed at 22:00 (open 09:00-18:00). Pick another time."}`
- Example request: "내일 10시 개신동 이비인후과 예약 저장해 줘."

## Tool: calculate
- Owner: (given — already implemented)
- File: src/tools/calculator.py
- Purpose: Evaluate a math expression. Use this for all prices, discounts, and totals.
- Type: compute
- Parameters: expression (string, required) — e.g. "7000 - 1500"
- Returns: `{"expression": "7000 - 1500", "result": 5500}`
- Errors: invalid expression → `{"error": "Invalid expression. Use numbers and + - * / ( ) only."}`
- Example request: "택시랑 버스 요금 차이가 얼마야?"
