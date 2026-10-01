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
