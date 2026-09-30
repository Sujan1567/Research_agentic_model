"""
Day 21 — Research Assistant (OpenAI Agents SDK)
===============================================

This is the SAME agent you built on Day 16 in n8n, rebuilt in Python.
Same three tools. Same system prompt. Different wrapper.

Run it:      python research_assistant.py
Ask it:      python research_assistant.py "What is the population of Pokhara?"

Before running, copy .env.example to .env and put your key in it.
"""

import os
import sys

from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings
from agents.exceptions import MaxTurnsExceeded

from tools import search_web, calculator, send_to_discord

load_dotenv()


# ---------------------------------------------------------------------------
# The system prompt.
#
# This is the seven-part structure from Day 13. Every heading is here on
# purpose. The two most commonly skipped are ESCALATION and OUTPUT FORMAT,
# and they are the two that cause trouble later.
#
# This text is copied word for word from the Day 16 n8n workflow (v2),
# so both versions give the agent exactly the same instructions.
# ---------------------------------------------------------------------------

INSTRUCTIONS = """\
ROLE
You are a research assistant for a small business in Kathmandu. You look things up, do the arithmetic, and report back clearly.

OBJECTIVE
Answer the user's question using your tools. You are finished when you have given a short, correct answer with the numbers checked.

TOOLS
- search_web: use this whenever the question needs current information you do not already know — prices, rates, facts about a place or company, recent events. Use it once or twice. Do not keep searching once you have a clear answer.
- calculator: use this for any arithmetic. Do not do sums in your head.
- send_to_discord: use this ONLY when the user explicitly asks you to send, share or post the result.

PROCESS
1. Work out what information you are missing.
2. Fetch it with search_web if it is not something you already know for certain.
3. Do any arithmetic with the calculator tool.
4. Give the final answer.

CONSTRAINTS
- Never invent a rate, a price, a date or a fact. If search_web returns nothing useful, say so.
- Never do arithmetic yourself. Always use the calculator tool.
- Keep the final answer under 80 words.
- Give all Nepali amounts in NPR.

ESCALATION
If a tool fails twice, or you cannot find the information after two searches, stop and say clearly what you could not do. Do not guess a substitute.

OUTPUT FORMAT
A short plain answer in 1 to 3 sentences. If you used a figure from a search, say where it came from and that it may not be exact real-time data.
"""


# ---------------------------------------------------------------------------
# The agent itself.
#
# Three lines. Compare this with the n8n canvas — same agent, different shape.
# ---------------------------------------------------------------------------

research_assistant = Agent(
    name="Research Assistant",
    instructions=INSTRUCTIONS,
    tools=[search_web, calculator, send_to_discord],
    # Say exactly which model runs, so you know what each question costs.
    # A low temperature (0.2) keeps the answers factual and steady.
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0.2),
)


def ask(question: str) -> str:
    """Run the agent once and return its final answer."""
    try:
        # Course rule 3: every agent has a limit. If the agent has not
        # finished after 10 turns of the loop, stop it instead of letting it
        # run (and spend money) forever.
        result = Runner.run_sync(research_assistant, question, max_turns=10)
        return result.final_output
    except MaxTurnsExceeded:
        return ("The agent stopped after 10 steps without finishing. "
                "Read the trace to see what it was doing.")


def main() -> None:
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = "Find the current USD to NPR rate and tell me what 850 dollars is worth."

    print("\nQUESTION")
    print(" ", question)
    print("\nWorking...\n")

    answer = ask(question)

    print("ANSWER")
    print(" ", answer)
    print()
    print("-" * 70)
    print("Now open the trace and read what it actually chose.")
    print("See developer-tools/04-reading-the-trace.md")
    print("-" * 70)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("\nNo OPENAI_API_KEY found.")
        print("Copy .env.example to .env and put your key in it.\n")
        sys.exit(1)
    if not os.getenv("TAVILY_API_KEY"):
        print("\nNote: no TAVILY_API_KEY found, so web search will not work.")
        print("Get a free key at tavily.com and add it to .env.\n")
    main()
