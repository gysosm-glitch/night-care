"""Helpers to read and write data/*.json files."""
import json

from src import config


def load(name: str) -> dict:
    """Read data/<name>.json and return it."""
    return json.loads((config.DATA_DIR / f"{name}.json").read_text(encoding="utf-8"))


def save(name: str, data: dict) -> None:
    """Write data to data/<name>.json."""
    (config.DATA_DIR / f"{name}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
