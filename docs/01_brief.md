# Project Brief

## Goal
Build a chat assistant for 충북대 students in Cheongju who get sick at night or on weekends.
The student types a question in natural language; the assistant uses **tools** to find an open clinic/pharmacy, the way to get there, and the cost.

## Users
A 충북대 student living in Cheongju. Not technical. Often tired, in a hurry, and unsure what is open.

## What the assistant can do
- Find clinics/pharmacies that are open **right now** for a symptom subject
- Show how to get there from 충북대 정문 (mode, minutes, fare, last bus)
- Estimate a taxi fare including the 22:00–04:00 night surcharge
- Save a visit plan (after asking the user to confirm)
- Calculate extra totals/comparisons

## Out of scope
- real APIs (공공데이터, bus), databases, payments, diagnosis, multiple users
- ALL data is fake demo data in `data/*.json`

## Why this is not a café agent (rename test)
Rename `find_open_places` → "is the latte open now?" and `estimate_taxi_cost` → "taxi fare for a coffee?": both are nonsense for a café.
A café owner never needs "open now at 23:10", "did the last bus already leave", or "night surcharge".

## Success criteria
- Never guesses hours, routes, or fares: all facts come from tools.
- Can answer questions that need 3 tools in a row.
- Recovers from tool errors (e.g. unknown subject) instead of crashing.
- Asks for confirmation before changing data (book_visit_plan).
