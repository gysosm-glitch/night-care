"""Command-line chat with the night-care agent."""
from src.agent import NightCareAgent


def main():
    agent = NightCareAgent()
    while True:
        text = input("You: ").strip()
        if text.lower() in ("exit", "quit"):
            break
        if text:
            print("Agent: " + agent.run(text))


if __name__ == "__main__":
    main()
