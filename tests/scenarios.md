# Test Scenarios

> 초안 (Claude 작성) — 팀 검토 후 이 줄을 지우세요.

Run `python -m src.main` and type each prompt. Compare the tool calls with the expected ones.
The exact order may vary slightly; what matters is that the agent uses tools instead of guessing.

## Required scenarios
| Kind | Example prompt | Expected tool calls | What to check |
|---|---|---|---|
| A. 3 tools in a row | 지금 밤 11시 10분인데 사창동까지 걸어가도 괜찮을까? | `estimate_walk_risk(사창동, 23:10)` → `get_route(사창동, 23:10)` → `estimate_taxi_cost(25, 23:10)` | 위험도 **82 (높음)**, 막차(22:30) 지남, 택시 **9,400원** 권유 |
| B. Error recovery | 밤 11시에 송정동 가는 길 안전해? | `estimate_walk_risk(송정동, 23:00)` → error(유효 지역 힌트) → 사용자에게 가능한 지역 안내 | 크래시/포기 없이 5개 동을 설명함 |
| C. Confirm before write | 내일(2026-10-02) 밤 11시에 정문에서 사창동까지 안심귀가 신청해 줘 | (확인 질문) → 사용자 "응" → `request_escort(사창동, 2026-10-02, 23:00, 충북대 정문, confirmed=true)` | "응" 전에는 `data/escort.json` 불변, 이후 E1 저장 |

## Extra scenarios
| Kind | Example prompt | Expected tool calls | What to check |
|---|---|---|---|
| D. Police box nearby | 밤 11시 반에 봉명동 근처 지구대 어디 있어? | `find_safe_spots(봉명동, 23:30)` | 봉명 지구대 이름·전화(043-270-3705)·주소 |
| E. Bus vs taxi | 사창동 가는 택시비랑 버스비 차이 계산해 줘 (밤 11시) | `get_route` → `estimate_taxi_cost` → `calculate(9400 - 1500)` | 차이 **7,900원** |
| F. Write error | 내일 저녁 8시에 안심귀가 신청해 줘 (사창동) | (확인) → `request_escort` → error(운영시간 22:00–01:00) → 다른 시간 또는 택시 제안 | 운영시간 안내 후 재제안 |
| H. Emergency | 지금 23:30이고 사창동인데 누가 따라오는 것 같아 | `get_emergency_guide(사창동, 23:30)` only (no risk analysis) | 첫 줄 "112에 전화", 사창 지구대 전화·주소, 112 문자 문구 |
| I. Trip + arrival | 지금 23:10인데 택시로 사창동 갈게. 기록해 줘 → "응" → "23:33 도착했어" | (확인) → `start_trip(사창동, 23:10, 택시, true)` → `check_arrival(T1, 23:33, true)` | ETA 23:35, 보호자 메시지, 도착 처리 |
| J. Overdue | (I 이후 도착 안 함) 00:00인데 아직 가는 중 | `check_arrival(T1, 00:00, false)` | overdue(25분 늦음) → 안전 확인 + 보호자 연락/112 권유 |
| K. Escort trust | 안심귀가 하면 어떤 사람이 와? 믿을 수 있어? | `get_escort_info()` | 선발 기준 + 만날 때 확인법, "데모 예시"라고 밝힘 (운영 중이라고 지어내지 않음) |
| G. Low risk | 오후 3시에 개신동 걸어가도 돼? | `estimate_walk_risk(개신동, 15:00)` | 낮음, 걸어가도 됨 (도보 8분) |

> After testing C/F/I/J, reset `data/escort.json` requests to `[]` and `data/trips.json` to `{"trips": []}`.

## Rename (reskin) test
| Our tool | Café rename | Result |
|---|---|---|
| find_safe_spots | which police box sells lattes? | nonsense |
| get_route (lights/CCTV) | how lit is the way to a croissant? | nonsense |
| estimate_walk_risk | risk score of walking to a coffee? | nonsense |
| estimate_taxi_cost | taxi fare for a coffee? | nonsense |
| get_escort_info | how are baristas background-checked to walk you home? | nonsense |
| request_escort | record_sale? | different logic (confirm + 운영시간 검사) |
| get_emergency_guide | what to text 112 about a latte? | nonsense |
| start_trip / check_arrival | did the coffee get home safely? | nonsense |
Verdict: good — 카페 에이전트에는 없는 도구가 4개.
