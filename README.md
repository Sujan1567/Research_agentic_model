# Day 21 — Research Assistant (OpenAI Agents SDK)

The same agent you built on Day 16 in n8n, rebuilt in Python.
Same three tools — web search, calculator and Discord — and the same system
prompt, word for word. Different wrapper.

Building it twice is deliberate. When you finish, put the two side by side
and you can see exactly what code gives you and what it costs you.

---

## Setup — five minutes

    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.example .env             # Windows: copy .env.example .env
                                     # then put your keys in .env

Make `.gitignore` **before** `.env`. If you create `.env` first and commit it,
the key is already in the history and deleting the file will not remove it.

---

## Run it

    python research_assistant.py
    python research_assistant.py "What is 200 EUR in GBP?"
    python run_examples.py           # the full demo sequence
    python run_examples.py 2         # just example 2

---

## What is in here

| File | What it is |
|---|---|
| `research_assistant.py` | The agent and its system prompt |
| `tools.py` | The three tools: `search_web`, `calculator`, `send_to_discord`. **Read the docstrings** |
| `run_examples.py` | Six questions to try, in teaching order |
| `.env.example` | Copy to `.env` and fill in your OpenAI key and your Tavily key |
| `developer-tools/` | Reference, options, limits, troubleshooting, experiments. Start at `00-START-HERE.md` |
| `explanation.md` | Both source files walked through block by block. **Read it with the code open beside it** |
| `prom.md` | The reusable prompts that produced this folder's docs |

---

## The one thing to notice today

Open `tools.py` and look at a docstring.

That docstring **is** the tool description. The framework reads your Python
and builds the tool definition from it. The model never sees your code —
only the function name, the docstring text above `Args:`, and the `Args:`
line for each parameter.

Notice what is missing from that list: the `Returns:` section. The SDK
drops it. That is why every failure message in `tools.py` carries its own
instruction ("Do not guess an answer") — the return value is the only place
the model will read it.

So a short lazy docstring breaks your agent, silently.

> On Day 13 you learned that a tool description is a prompt.
> Here, your docstring **is** the prompt.

---

## Three exercises

**1. Compare it with n8n.** Fill in the table in
`developer-tools/06-comparison-with-n8n.md`. There is no right answer —
the point is learning what each approach actually costs you.

**2. Break it.** Replace one docstring with `"""Gets data."""` and run
example 2 again. Watch the agent ignore the tool or use it wrongly.
You deleted a comment and broke the agent.

**3. See what the model sees.** Run this and read the output:

    python -c "import tools; print(tools.search_web.description); print(tools.search_web.params_json_schema)"

You should see the opening text and the `query` description — and no
`Returns:` section anywhere. Anything you want the model to know must live
above `Args:`, in an `Args:` line, or in the string the tool returns.

---

## If something goes wrong

See `developer-tools/05-troubleshooting.md`. Check the model tag and the
`.env` file first — that is most of it.
