"""The agent: keeps conversation history and runs the tool-calling loop."""
import json

from src import config
from src.llm_client import chat
from src.tools import TOOL_FUNCTIONS, TOOL_SCHEMAS


class NightCareAgent:
    def __init__(self):
        self.system_prompt = config.SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
        self.history: list = []  # user, assistant, and tool messages (NOT the system prompt)
        self.tool_log: list = []  # (name, args, result) of the last run(), for the UI

    def _build_context(self) -> list:
        """Return the messages to send to the LLM: system prompt + (trimmed) history."""
        history = self.history[-config.MAX_HISTORY_MESSAGES:]
        # never start with an orphan tool message (its assistant tool_call was trimmed away)
        while history and history[0].get("role") == "tool":
            history = history[1:]
        return [{"role": "system", "content": self.system_prompt}] + history

    def _execute_tool(self, name: str, arguments_json: str) -> dict:
        """Run one tool safely. Never raise: return {"error": ...} on any problem."""
        func = TOOL_FUNCTIONS.get(name)
        if func is None:
            return {"error": f"Unknown tool '{name}'. Valid: {sorted(TOOL_FUNCTIONS)}."}
        try:
            args = json.loads(arguments_json or "{}")
            return func(**args)
        except Exception as exc:  # noqa: BLE001
            return {"error": f"Tool '{name}' failed: {exc}"}

    def run(self, user_input: str) -> str:
        """Handle one user message and return the final answer text."""
        self.tool_log = []
        self.history.append({"role": "user", "content": user_input})
        for _ in range(config.MAX_TOOL_ROUNDS):
            msg = chat(self._build_context(), TOOL_SCHEMAS)
            entry = {"role": "assistant", "content": msg.content or ""}
            if msg.tool_calls:
                entry["tool_calls"] = [
                    {"id": t.id, "type": "function",
                     "function": {"name": t.function.name, "arguments": t.function.arguments}}
                    for t in msg.tool_calls
                ]
            self.history.append(entry)
            if not msg.tool_calls:
                return msg.content or ""
            for t in msg.tool_calls:
                result = self._execute_tool(t.function.name, t.function.arguments)
                print(f"  [tool] {t.function.name}({t.function.arguments}) -> {result}")
                self.tool_log.append((t.function.name, t.function.arguments, result))
                self.history.append({"role": "tool", "tool_call_id": t.id,
                                     "content": json.dumps(result, ensure_ascii=False)})
        return "Sorry, I could not finish this request."
