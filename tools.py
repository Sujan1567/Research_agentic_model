"""
The three tools.
================

Read the docstrings carefully. In this framework the docstring IS the tool
description — the framework reads it and shows it to the model.

That means a lazy docstring directly breaks the agent, and it does so
silently. This is the Day 13 lesson, arriving in Python.

Each docstring here says four things:
    1. what the tool does
    2. when to use it, and when NOT to
    3. what it returns
    4. what an empty or failed result means
"""

import os

import requests
from agents import function_tool


# ---------------------------------------------------------------------------
# Tool 1 — web search (Tavily)
# This is the SAME search service used by the Day 16 n8n workflow (v2),
# so the n8n version and this Python version can be compared fairly.
# ---------------------------------------------------------------------------

@function_tool
def search_web(query: str) -> str:
    """Search the web for current information — prices, exchange rates, facts about a place, company or event.

    Use this whenever the question needs something you cannot know for certain
    from memory alone. Use it once, or twice at most. If the first results
    already answer the question, stop searching.
    Do NOT use it for arithmetic — use the calculator tool for that.

    Args:
        query: what to search for. Be specific, and keep it under 12 words.
            For example: USD to NPR exchange rate today

    Returns:
        Up to 5 search results, each with a title, a link and a short summary.
        If nothing useful is found, it says so in words. That is a real answer —
        it means the information could not be found. Do not invent a value to
        fill the gap.
    """
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        return (
            "No Tavily API key is configured, so the search could not run. "
            "Tell the user the search is unavailable. Do not guess an answer."
        )

    try:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={"Authorization": f"Bearer {key}"},
            json={"query": query, "max_results": 5, "search_depth": "basic"},
            timeout=15,
        )
    except requests.RequestException as error:
        return f"Could not reach the search service: {error}"

    if response.status_code == 401:
        return "The search service rejected the API key (status 401). Check TAVILY_API_KEY."
    if response.status_code != 200:
        return f"The search service refused the request (status {response.status_code})."

    results = response.json().get("results", [])
    if not results:
        return "No results were found for that search. Say so rather than guessing."

    lines = []
    for number, item in enumerate(results, start=1):
        summary = (item.get("content") or "").strip().replace("\n", " ")[:300]
        lines.append(f"{number}. {item.get('title', 'No title')}\n   {item.get('url', '')}\n   {summary}")
    return "\n\n".join(lines)


# ---------------------------------------------------------------------------
# Tool 2 — calculator
# ---------------------------------------------------------------------------

@function_tool
def calculator(expression: str) -> str:
    """Do arithmetic. Use this for every calculation, including simple ones.

    Models are unreliable at arithmetic, especially with long numbers, so
    always use this rather than working it out yourself.

    Args:
        expression: a plain maths expression as text, for example: 850 * 133.4
            Allowed: digits, decimal points, and + - * / ( )
            Not allowed: words, currency symbols, commas in numbers,
            or ** (powers).

    Returns:
        The answer as a number, rounded to two decimal places.
        If the expression is not valid maths it returns an error message
        explaining what was wrong. Fix the expression and try once more.
    """
    cleaned = expression.strip().replace(",", "")

    allowed = set("0123456789+-*/(). ")
    # Block ** (powers): something like 9**9**9 is so large that the
    # program would freeze trying to calculate it. Also cap the length.
    if "**" in cleaned or len(cleaned) > 100:
        return "That expression is not allowed. Use only + - * / ( ) and keep it short."

    if not cleaned or not set(cleaned).issubset(allowed):
        return (
            "That is not a valid maths expression. "
            "Send only numbers and the symbols + - * / ( ) ."
        )

    try:
        result = eval(cleaned, {"__builtins__": {}}, {})
    except Exception as error:
        return f"Could not calculate that: {error}"

    if not isinstance(result, (int, float)):
        return "That expression did not produce a number."

    return str(round(float(result), 2))


# ---------------------------------------------------------------------------
# Tool 3 — send to Discord
# ---------------------------------------------------------------------------

@function_tool
def send_to_discord(message: str) -> str:
    """Send a short message to the team's Discord channel.

    Use this ONLY when the user explicitly asks you to send, post, share or
    notify. Do NOT use it to show the user their answer — simply reply
    normally for that.

    Args:
        message: the message to post. Keep it under 200 characters.

    Returns:
        "sent" if it worked, or an error message explaining what failed.
        If it fails, tell the user rather than pretending it was sent.
    """
    webhook = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook:
        return (
            "No Discord webhook is configured, so nothing was sent. "
            "Tell the user the message could not be delivered."
        )

    try:
        response = requests.post(webhook, json={"content": message}, timeout=10)
    except requests.RequestException as error:
        return f"Could not reach Discord: {error}"

    if response.status_code not in (200, 204):
        return f"Discord refused the message (status {response.status_code})."

    return "sent"
