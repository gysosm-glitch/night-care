# Project Brief

> 초안 (Claude 작성) — 팀 검토 후 이 줄을 지우세요.

## Goal
Build a chat assistant that helps 충북대 students in Cheongju **get home safely at night**.
The student types a question in natural language; the assistant uses **tools** to check how risky the walk is, where the nearest open safe spot is, whether a bus is still running, what a taxi costs, and can file a 안심귀가 escort request.

## Users
A 충북대 student (often living alone near 개신동/사창동/복대동/봉명동/율량동) going home after a late class, part-time job, or club meeting. Not technical. Often walking alone, possibly anxious, and wants a quick, clear answer.

## What the assistant can do
- Find **safe spots open right now** in a district (지구대·파출소, 24시 편의점, 안심지킴이집)
- Show the way home from 충북대 정문: walking minutes, streetlight ratio, CCTV count, bus line and last bus
- **Score the walking risk (0–100)** for a district at a given time and explain why
- Estimate a taxi fare including the 22:00–04:00 night surcharge
- Save a **안심귀가 escort request** (only after the user confirms; only within service hours)
- Calculate extra totals/comparisons (e.g. bus vs taxi)

## Out of scope
- real APIs (경찰청, 공공데이터, bus, map), real-time location tracking, calling 112 for the user, payments, multiple users
- ALL data is fake demo data in `data/*.json`
- The assistant never says a route is "100% safe". In a real emergency it tells the user to call **112**.

## Why this is not a café agent (rename test)
Rename `estimate_walk_risk` → "how risky is it to walk to the latte?" and `find_safe_spots` → "which police box sells croissants?": both are nonsense for a café.
A café owner never needs "is it dark and empty at 23:30", "is a police box open nearby", or "book someone to walk me home".

## Success criteria
- Never guesses hours, routes, risk scores, or fares: all facts come from tools.
- Can answer questions that need 3 tools in a row (risk → safe spots/route → taxi).
- Recovers from tool errors (e.g. unknown district, escort outside service hours) instead of crashing.
- Asks for confirmation before changing data (`request_escort`).
