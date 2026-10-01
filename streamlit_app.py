"""Streamlit Cloud entry point. Runs src/app.py from the repo root so `from src...` imports work."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).parent / "src" / "app.py"), run_name="__main__")
