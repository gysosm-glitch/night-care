"""Streamlit Cloud entry point. Runs src/app.py from the repo root so `from src...` imports work."""
import os
import runpy
from pathlib import Path

import streamlit as st

# Streamlit Cloud keeps keys in st.secrets; config.py reads env vars, so copy them over.
try:
    for key, value in st.secrets.items():
        if isinstance(value, str):
            os.environ.setdefault(key, value)
except Exception:
    pass  # no secrets.toml (local run) -> config.py falls back to .env

runpy.run_path(str(Path(__file__).parent / "src" / "app.py"), run_name="__main__")
