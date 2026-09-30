# 1. Setup guide

## Requirements

- Python 3.10 or newer  (check with `python --version`)
- An API key from a model provider
- A Tavily API key for web search (free plan at tavily.com)
- About five minutes

---

## Step by step

### 1. A virtual environment

    python -m venv .venv

    source .venv/bin/activate        # macOS / Linux
    .venv\Scripts\activate           # Windows

Your prompt should now start with `(.venv)`. If it does not, the environment
is not active and `pip install` will go to the wrong place.

### 2. Install

    pip install -r requirements.txt

### 3. `.gitignore` FIRST

Before you create `.env`, make sure `.gitignore` exists and contains `.env`.

This order matters. If you create `.env` first, commit it, then add
`.gitignore`, the key is already in your git history. Deleting the file does
not remove it — you would have to revoke the key.

### 4. `.env`

    cp .env.example .env

Then open `.env` and paste your OpenAI key and your Tavily key.

The Tavily key is the same one you used in the Day 16 n8n workflow (v2).
Here it lives in `.env`, not inside a node — the safe way from Day 7.

### 5. Check it works

    python research_assistant.py "hello"

---

## Using a local model instead

The name is misleading — this SDK is not limited to OpenAI models. It works
with anything that speaks the OpenAI chat format, which includes your Ollama
model from Day 4.

    from openai import AsyncOpenAI
    from agents import OpenAIChatCompletionsModel

    local_client = AsyncOpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )

    agent = Agent(
        name="Research Assistant",
        instructions=INSTRUCTIONS,
        tools=[...],
        model=OpenAIChatCompletionsModel(
            model="qwen3:4b",
            openai_client=local_client,
        ),
    )

This is Day 4's one-line switch, still applying. Prototype locally for free,
move to a frontier model when quality demands it.

**Expect worse tool selection on a small local model.** That is not a bug —
it is Day 4's finding that small models fail on instruction-following more
than on knowledge.
