# Test Scenarios

Run `python -m src.main` and type each prompt. Compare the tool calls with the expected ones.
The exact order may vary slightly; what matters is that the agent uses tools instead of guessing.
(Written BEFORE the tools were built — Task 5.)

## Required scenarios
| Kind | Example prompt | Expected tool calls | What to check |
|---|---|---|---|
| A. 3 tools in a row | 지금 밤 11시 10분인데 열이 나. 갈 곳이랑 택시비 알려줘 | `find_open_places(23:10, 내과)` → `get_route(사창동, 23:10)` → `estimate_taxi_cost(25, 23:10)` | 응급의료센터(사창동) 추천, 막차(22:30) 지남, 택시 심야할증 적용 **9,400원** |
| B. Error recovery | 밤 11시인데 치과 열린 곳 있어? | `find_open_places(23:00, 치과)` → error(유효 과목 힌트) → 다른 과목으로 재시도 또는 사용자에게 안내 | 크래시/포기 없이 가능한 과목을 설명함 |
| C. Confirm before write | 내일(2026-10-02) 10시에 개신동 이비인후과 예약 저장해 줘 | (확인 질문) → 사용자 "응" → `book_visit_plan(C3, ..., confirmed=true)` | "응" 전에는 `data/visit_plans.json` 불변, 이후 P1 저장 |

## Extra scenarios
| Kind | Example prompt | Expected tool calls | What to check |
|---|---|---|---|
| D. Bus still running | 밤 9시에 복대동 약국 가려는데 버스 있어? | `find_open_places(21:00, 일반의약품)` → `get_route(복대동, 21:00)` | 복대동 약국이 없으면 열린 약국(개신동·사창동)을 안내하고 버스 가능 여부를 정확히 설명 |
| E. Bus vs taxi | 사창동 가는 택시비랑 버스비 차이 계산해 줘 (밤 11시) | `get_route` → `estimate_taxi_cost` → `calculate(9400 - 1500)` | 차이 **7,900원** |
| F. Write error | 내일 밤 10시 개신동 이비인후과 예약해 줘 | (확인) → `book_visit_plan` → error(운영시간 외) → 다른 시간 제안 | 운영시간(09–18시) 안내 후 재제안 |

> After testing C/F, reset `data/visit_plans.json` to `{"plans": []}`.

## Rename (reskin) test
| Our tool | Café rename | Result |
|---|---|---|
| find_open_places | is the latte open now? | nonsense |
| get_route | route to a croissant? | nonsense |
| estimate_taxi_cost | taxi fare for a coffee? | nonsense |
| book_visit_plan | record_sale? | different logic (confirm + 운영시간 검사) |
Verdict: good — 카페 에이전트에는 없는 도구가 3개.
