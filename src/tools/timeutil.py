"""Small helper: parse "HH:MM" (24:00 allowed) into minutes since midnight."""
import re


def to_minutes(text: str) -> int | None:
    """Return minutes since midnight for 'HH:MM', or None if the text is not a valid time."""
    match = re.fullmatch(r"(\d{1,2}):(\d{2})", str(text).strip())
    if not match:
        return None
    h, m = int(match.group(1)), int(match.group(2))
    if m > 59 or h > 24 or (h == 24 and m > 0):
        return None
    return h * 60 + m


def in_window(now: int, start: str, end: str) -> bool:
    """True if `now` (minutes) is in [start, end). Handles windows that cross midnight, e.g. 22:00-01:00."""
    s, e = to_minutes(start), to_minutes(end)
    if s <= e:
        return s <= now < e
    return now >= s or now < e
