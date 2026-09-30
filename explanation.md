# How the research assistant works, block by block

This walks through the two files that make the agent. `research_assistant.py`
builds the agent and runs it. `tools.py` holds the three functions it may call.

**How each block is laid out below:**

1. the code itself,
2. **What this block does** — the purpose, in plain English,
3. **Line by line** — every piece of syntax,
4. sometimes **Why it is written this way** — the design reason.

---

# Part 1 — research_assistant.py

> It loads your API key, writes down the agent's instructions, builds the
> agent object out of those instructions plus three tools, and gives you two
> ways to run it — `ask()` for other code, and `main()` for the command line.

## 1.1 The module docstring

```python
"""
Day 21 — Research Assistant (OpenAI Agents SDK)
===============================================

This is the SAME agent you built on Day 16 in n8n, rebuilt in Python.
Same three tools. Same system prompt. Different wrapper.

Run it:      python research_assistant.py
Ask it:      python research_assistant.py "What is the population of Pokhara?"

Before running, copy .env.example to .env and put your key in it.
"""
```

**What this block does:** it is the file's front page. Anyone who opens the
file learns what it is, how to run it, and the one setup step they must do
first — before reading a line of code.

**Line by line:**

- `"""` ... `"""` is a **triple-quoted string**: a string that can run over
  many lines.
- Because it is the very first statement in the file, Python treats it as the
  **module docstring**. It is stored on the module as `__doc__`, so
  `import research_assistant; print(research_assistant.__doc__)` prints it.
- The `=====` underline is plain text. It only makes the title stand out.

---

## 1.2 The imports

```python
import os
import sys

from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings
from agents.exceptions import MaxTurnsExceeded

from tools import search_web, calculator, send_to_discord
```

**What this block does:** it gathers everything the file uses from elsewhere —
two pieces of Python itself, five names from installed libraries, and the three
tools from this project.

**Line by line:**

- `import os` brings in the operating-system module. The file uses it for
  `os.getenv`, which reads an **environment variable** — a named value that
  lives outside your code.
- `import sys` brings in the system module. The file uses `sys.argv` (the
  words typed after the script name) and `sys.exit` (stop the program).
- `from dotenv import load_dotenv` takes one function from the `python-dotenv`
  package. Note the package is installed as `python-dotenv` but imported as
  `dotenv`.
- `from agents import Agent, Runner, ModelSettings` takes three names from the
  OpenAI Agents SDK. Again the names differ: you `pip install openai-agents`
  but `import agents`.
  - `Agent` describes an agent: a model, its instructions and its tools.
  - `Runner` runs that agent through its loop.
  - `ModelSettings` holds tuning values such as temperature.
- `from agents.exceptions import MaxTurnsExceeded` takes one **exception** —
  an error type — that the SDK raises when an agent runs out of turns.
- `from tools import ...` imports the three tool functions from `tools.py` in
  this same folder.

**Why it is written this way:** the imports sit in three groups separated by
blank lines — the standard library first, then installed packages, then this
project's own files. That is the convention from PEP 8, Python's style guide.
It lets you see at a glance what must be installed (group two) and what lives
in the project (group three).

---

## 1.3 Loading the `.env` file

```python
load_dotenv()
```

**What this block does:** it copies your keys out of the `.env` file and into
the environment, so the rest of the program can read them with `os.getenv`.

**Line by line:**

- `load_dotenv()` looks for a file called `.env`, reads each `NAME=value`
  line, and sets it as an environment variable for this running program.
- By default it does **not** overwrite a variable that is already set. If
  your shell already has `OPENAI_API_KEY`, that one wins over the file.

**Why it is written this way:** this line sits at the top level of the file,
not inside a function. That means it runs at **import time** — the moment any
other file does `import research_assistant`. So `run_examples.py`, which only
imports `ask`, still gets the keys loaded. Keys live in `.env` rather than in
the code so that the code can be shared, committed and shown on screen
without leaking a secret.

---

## 1.4 The system prompt

```python
INSTRUCTIONS = """\
ROLE
You are a research assistant for a small business in Kathmandu. You look things up, do the arithmetic, and report back clearly.

OBJECTIVE
Answer the user's question using your tools. You are finished when you have given a short, correct answer with the numbers checked.

TOOLS
- search_web: use this whenever the question needs current information you do not already know — prices, rates, facts about a place or company, recent events. Use it once or twice. Do not keep searching once you have a clear answer.
- calculator: use this for any arithmetic. Do not do sums in your head.
- send_to_discord: use this ONLY when the user explicitly asks you to send, share or post the result.
...
OUTPUT FORMAT
A short plain answer in 1 to 3 sentences. If you used a figure from a search, say where it came from and that it may not be exact real-time data.
"""
```

**What this block does:** it is the agent's job description. Every time the
agent runs, this text goes to the model first, and it decides who the agent
is, which tool to use when, what it must never do, and what the answer should
look like.

**Line by line:**

- `INSTRUCTIONS` is in ALL CAPS. That is the Python convention for a
  **constant** — a value set once and never changed while the program runs.
  Python does not enforce it; it is a signal to the reader.
- `"""\` opens a triple-quoted string. The **backslash** right after the
  quotes cancels the line break, so the string starts with `ROLE` instead of
  with an empty line.
- Each long line is left unwrapped on purpose. Line breaks inside the string
  would be sent to the model as part of the text.
- The comment block above it (not shown) records that this text is copied
  word for word from the Day 16 n8n workflow, so the two versions can be
  compared fairly.

The seven headings are the Day 13 structure:

| Heading | What it is for | What breaks without it |
|---|---|---|
| `ROLE` | Who the agent is and who it serves | Answers drift in tone and scope; it stops sounding like a business tool |
| `OBJECTIVE` | When the job is finished | It keeps searching after it already has the answer |
| `TOOLS` | When to use each tool — and when not to | It posts to Discord unasked, or answers a rate question from memory |
| `PROCESS` | The order of steps | It calculates before it has fetched the rate it needs |
| `CONSTRAINTS` | Hard rules: never invent, never do sums in its head, under 80 words, NPR | It makes up a plausible exchange rate and multiplies it wrongly |
| `ESCALATION` | When to stop and admit it could not do it | It loops on a failing tool, or quietly guesses a substitute value |
| `OUTPUT FORMAT` | The shape of the final answer | Long, inconsistent answers with no hint that a rate may be out of date |

**Why it is written this way:** the `TOOLS` section repeats, in shorter form,
what each tool's docstring says. That repetition is deliberate. The docstring
tells the model what a tool *is*; the instructions tell it how the tools fit
together in *this* job. The comment above it points out that `ESCALATION` and
`OUTPUT FORMAT` are the two most often skipped — and the two that cause the
most trouble later.

---

## 1.5 Creating the agent

```python
research_assistant = Agent(
    name="Research Assistant",
    instructions=INSTRUCTIONS,
    tools=[search_web, calculator, send_to_discord],
    # Say exactly which model runs, so you know what each question costs.
    # A low temperature (0.2) keeps the answers factual and steady.
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0.2),
)
```

**What this block does:** it builds the agent itself — one object that
bundles the model, the instructions and the tools. Nothing runs yet. This
only describes the agent; `Runner` brings it to life later.

**Line by line:**

- `Agent(...)` creates an `Agent` object. Every value is passed as a
  **keyword argument** — `name=...` — so the order does not matter and each
  value is labelled.
- `name="Research Assistant"` is the label that shows up in traces. With
  several agents, it is how you tell them apart.
- `instructions=INSTRUCTIONS` hands over the system prompt from 1.4.
- `tools=[search_web, calculator, send_to_discord]` is a **list** of the three
  tool objects. The agent may call these and nothing else.
- `model="gpt-4o-mini"` names the model exactly. Leave it out and you get the
  SDK's default, which can change when you upgrade the package.
- `model_settings=ModelSettings(temperature=0.2)` sets the **temperature** —
  how much randomness the model uses when choosing its words. `0` is the most
  repeatable; higher values vary more. `0.2` is low: steady, factual answers.

**Why it is written this way:** the model is named explicitly so that you
know what each question costs and so that the behaviour does not change under
you. This whole block is the Python equivalent of the n8n AI Agent node with
its sub-nodes plugged in — the comment above it in the file asks you to
compare the two shapes.

---

## 1.6 The `ask` function — its signature

```python
def ask(question: str) -> str:
    """Run the agent once and return its final answer."""
```

**What this block does:** it declares the one function other code should
call. Give it a question, get back an answer as text. `run_examples.py` uses
exactly this and nothing else.

**Line by line:**

- `def ask(question: str) -> str:` defines a function named `ask` with one
  parameter, `question`.
- `: str` after the parameter and `-> str` after the brackets are **type
  hints**. They say "takes text, returns text". Python does not enforce them
  at runtime; they are documentation that your editor can check.
- The one-line `"""..."""` is the function's **docstring**. Here it is only
  for human readers. (In `tools.py`, docstrings do real work — see Part 2.)

---

## 1.6b The `ask` function — running the agent with a limit

```python
    try:
        # Course rule 3: every agent has a limit. If the agent has not
        # finished after 10 turns of the loop, stop it instead of letting it
        # run (and spend money) forever.
        result = Runner.run_sync(research_assistant, question, max_turns=10)
        return result.final_output
    except MaxTurnsExceeded:
        return ("The agent stopped after 10 steps without finishing. "
                "Read the trace to see what it was doing.")
```

**What this block does:** it runs the agent's loop — ask the model, run any
tool it picks, feed the result back, repeat — until the model gives a final
answer. If that takes more than 10 rounds, it stops the agent and returns a
plain explanation instead of crashing.

**Line by line:**

- `try:` ... `except MaxTurnsExceeded:` is **exception handling**. Python runs
  the `try` part; if that specific error is raised inside it, Python jumps to
  the `except` part instead of stopping the program.
- `Runner.run_sync(...)` runs the agent and **blocks** — waits — until it is
  finished. `sync` is short for synchronous. The SDK also has `Runner.run`,
  which you `await` in asynchronous code.
- Its three arguments: the agent from 1.5, the user's question, and
  `max_turns=10`.
- `max_turns=10` caps the number of model calls in one run. One "turn" is one
  trip to the model, whether it answers or asks for a tool.
- `result.final_output` is the model's final answer. `result` also holds
  everything that happened along the way, in `result.new_items`.
- The `except` branch returns a sentence rather than raising. The caller
  always gets a string back, just as the type hint promised.
- The two strings in brackets sit side by side with no `+` between them.
  Python joins **adjacent string literals** automatically, so this is one
  string split over two lines.

**Why it is written this way:** an agent decides for itself when to stop, so
nothing guarantees it ever will. Without the limit, a tool that keeps failing
could make the model retry forever, and each retry is a paid API call. `10`
happens to be the SDK's own default, but writing it out makes the limit
visible and easy to change.

Note what is deliberately *not* caught: a missing or wrong API key, a network
failure, or a model name that does not exist. Those raise their normal errors,
because they are setup mistakes you should see in full, not paper over.

---

## 1.7 The `main` function — choosing the question

```python
def main() -> None:
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = "Find the current USD to NPR rate and tell me what 850 dollars is worth."
```

**What this block does:** it decides what to ask. If you typed a question
after the script name, it uses yours; if not, it uses the main demo question.

**Line by line:**

- `-> None` says the function returns nothing. It prints instead.
- `sys.argv` is a list of the words on the command line. For
  `python research_assistant.py What is 2+2`, it is
  `["research_assistant.py", "What", "is", "2+2"]`. The first item is always
  the script name.
- `len(sys.argv) > 1` is true when you typed anything after the script name.
- `sys.argv[1:]` is a **slice**: everything from position 1 to the end, which
  drops the script name. Here that is `["What", "is", "2+2"]`.
- `" ".join([...])` glues a list of strings together with a space between
  each: `" ".join(["What", "is", "2+2"])` gives `"What is 2+2"`. This is why
  the question works with or without quotes around it.

---

## 1.7b The `main` function — running it and showing the answer

```python
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
```

**What this block does:** it shows the question, runs the agent through
`ask`, shows the answer, and then points you at the trace — the record of
what the agent actually did — because the answer alone does not tell you how
it got there.

**Line by line:**

- `"\n"` is a **newline** character, so `"\nQUESTION"` prints a blank line
  and then `QUESTION`.
- `print(" ", question)` passes two values. `print` separates them with a
  space, so the question comes out indented by two spaces.
- `"Working..."` is printed before the slow part so you know it has not
  frozen. A run with a search and a calculation takes several seconds.
- `answer = ask(question)` — `main` reuses `ask` rather than calling `Runner`
  itself. There is one place that runs the agent, not two.
- `print()` with nothing inside prints an empty line.
- `"-" * 70` repeats a string: it gives seventy dashes, a separator line.

---

## 1.8 The entry point and its safety checks

```python
if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("\nNo OPENAI_API_KEY found.")
        print("Copy .env.example to .env and put your key in it.\n")
        sys.exit(1)
    if not os.getenv("TAVILY_API_KEY"):
        print("\nNote: no TAVILY_API_KEY found, so web search will not work.")
        print("Get a free key at tavily.com and add it to .env.\n")
    main()
```

**What this block does:** it runs only when you launch this file directly. It
checks your keys before doing anything costly — refusing to start without the
OpenAI key, and warning (but carrying on) without the Tavily key — and then
calls `main()`.

**Line by line:**

- `__name__` is a variable Python sets for every file. It is `"__main__"`
  when you run the file (`python research_assistant.py`) and
  `"research_assistant"` when another file imports it. So this **guard** means
  "only when run directly".
- `os.getenv("OPENAI_API_KEY")` returns the value, or `None` if it is not set.
- `not ...` is true for `None` and for an empty string `""`. Both are
  **falsy** — values Python treats as false in an `if`. So a line
  `OPENAI_API_KEY=` with nothing after it counts as missing too.
- `sys.exit(1)` stops the program with **exit code** `1`. By convention `0`
  means success and anything else means failure, which scripts and CI systems
  can check.
- The Tavily check has no `sys.exit`. The agent can still answer some
  questions without search, so it warns and carries on.

**Why it is written this way:** this is a **fail-fast** check. Without it, a
missing key surfaces as a long SDK stack trace halfway through a run. With it,
you get one plain sentence that says what to do. The guard also matters for
`run_examples.py`: because it imports `ask`, the guard stops `main()` from
running a second, unwanted question on import. The flip side is that
`run_examples.py` skips these key checks too, so a missing key there shows
the raw SDK error.

---

# Part 2 — tools.py

> It defines three ordinary Python functions — search the web, do arithmetic,
> post to Discord — and marks each with `@function_tool` so the SDK can offer
> it to the model, using the docstring as the tool's description.

## 2.1 The module docstring

```python
"""
The three tools.
================

Read the docstrings carefully. In this framework the docstring IS the tool
description — the framework reads it and shows it to the model.
...
Each docstring here says four things:
    1. what the tool does
    2. when to use it, and when NOT to
    3. what it returns
    4. what an empty or failed result means
"""
```

**What this block does:** it tells you the single most important fact about
this file before you read any of it: in this framework, a docstring is not a
comment for humans — it is a prompt the model reads.

**Line by line:**

- Like 1.1, it is the module docstring because it is the first statement.
- The four-point checklist is the standard every tool below is written to.

**Why it is written this way:** one correction, checked against the installed
SDK (`openai-agents` 0.22). The model sees the docstring text **above**
`Args:` and each line **under** `Args:`. The `Returns:` section is parsed and
then dropped — the model never reads it. Points 3 and 4 of the checklist
still reach the model in this file, but through a different route: every
failure path returns a sentence that says what it means ("Say so rather than
guessing"). You can see exactly what the model gets with
`print(tools.search_web.description)`.

---

## 2.2 The imports

```python
import os

import requests
from agents import function_tool
```

**What this block does:** it brings in the three things the tools need —
environment variables for the keys, an HTTP library to call the outside
services, and the decorator that turns a function into a tool.

**Line by line:**

- `import os` — for `os.getenv`, to read `TAVILY_API_KEY` and
  `DISCORD_WEBHOOK_URL`.
- `import requests` — the standard third-party library for making web
  requests. It sits in its own group because it must be installed.
- `from agents import function_tool` — the **decorator** from the SDK.

Notice there is no `load_dotenv()` here. The keys are read inside each tool,
at the moment it runs, and by then `research_assistant.py` has already loaded
the `.env` file.

---

## 2.3 Tool 1 — `search_web`

**What this whole tool is for:** it fetches current facts the model cannot
know from memory — today's exchange rate, a population figure — using the
Tavily search API, and hands back up to five short results as text.

### 2.3a The decorator and signature

```python
@function_tool
def search_web(query: str) -> str:
```

**What this block does:** it declares an ordinary function and, with one
line on top, registers it as a tool the model can call.

**Line by line:**

- `@function_tool` is a **decorator**: a line starting with `@` placed above
  a function. It takes the function and replaces it with something built from
  it. Here it replaces `search_web` with a `FunctionTool` object that the
  `Agent` can use.
- To build that object, the decorator reads three things: the function name
  (`search_web` becomes the tool's name), the docstring (the description),
  and the parameters and type hints (`query: str` becomes "one required text
  argument called `query`").
- `-> str` matters here: the model can only read text, so every tool in this
  file returns a string.

### 2.3b The docstring — the tool's description

```python
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
        ...
    """
```

**What this block does:** it is the prompt the model reads when it decides
whether to search, and what to type into the search box. Change this text and
you change the agent's behaviour, without touching a line of code.

**Line by line:**

- The first line says **what** it does, with examples of the kind of thing
  it finds.
- "Use this whenever..." says **when**. "Use it once, or twice at most"
  and "stop searching" stop it looping. "Do NOT use it for arithmetic" says
  when **not** to — and names the tool to use instead.
- `Args:` starts a **Google-style** docstring section. The SDK matches
  `query:` to the `query` parameter and sends that text as the parameter's
  description. "Under 12 words" and the example value shape the search the
  model writes.
- `Returns:` describes the output for human readers. As 2.1 explains, the
  SDK does not send this part to the model.

**Why it is written this way:** the model never sees the code below. If the
docstring only said `"""Searches."""`, the model would not know what it
searches, when it should, or when to stop — and nothing would raise an error
to tell you. The breakage would be silent.

### 2.3c Checking for the key

```python
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        return (
            "No Tavily API key is configured, so the search could not run. "
            "Tell the user the search is unavailable. Do not guess an answer."
        )
```

**What this block does:** if there is no Tavily key, it gives up at once and
tells the model — in words — what that means and what to do about it.

**Line by line:**

- `os.getenv("TAVILY_API_KEY")` returns the key, or `None`.
- `if not key:` is true for `None` or an empty string (both falsy).
- The `return` sends back a sentence rather than raising an error. The last
  sentence, "Do not guess an answer", is an instruction to the model riding
  inside the tool result.

**Why it is written this way:** the key is read inside the function, at call
time, not once at the top of the file. So the tool always sees the current
environment, and importing `tools.py` never fails just because a key is
missing. Returning text rather than raising is covered in 2.3d.

### 2.3d Calling the search service

```python
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={"Authorization": f"Bearer {key}"},
            json={"query": query, "max_results": 5, "search_depth": "basic"},
            timeout=15,
        )
    except requests.RequestException as error:
        return f"Could not reach the search service: {error}"
```

**What this block does:** it sends the search to Tavily over the internet,
with a time limit, and turns any network failure into a sentence for the
model instead of a crash.

**Line by line:**

- `requests.post(url, ...)` sends an HTTP **POST** request — a request that
  carries data — and returns a `response` object.
- `headers={"Authorization": f"Bearer {key}"}` sends the key the way Tavily
  expects it. `f"..."` is an **f-string**: `{key}` is replaced by the value of
  `key`, so the header becomes `"Bearer tvly-abc..."`.
- `json={...}` turns the dictionary into JSON and sends it as the request
  body: the search text, at most 5 results, and the cheaper `"basic"` depth.
- `timeout=15` gives up if the server has not responded within 15 seconds.
- `except requests.RequestException as error:` catches every error `requests`
  can raise — no connection, DNS failure, timeout — and names it `error`.
- `f"Could not reach the search service: {error}"` returns the error's own
  message inside a sentence.

**Why it is written this way:** `requests` has **no timeout by default**.
Without `timeout=15`, a hung server can freeze your agent indefinitely, and
the `max_turns` limit cannot help, because the turn never ends.

Returning a string instead of raising matters too. If a tool raises, the SDK
catches it and sends the model its own generic message: "An error occurred
while running the tool. Please try again." That invites exactly the retry
loop you are trying to prevent. Returning your own sentence lets you say what
actually happened.

### 2.3e Checking the status code

```python
    if response.status_code == 401:
        return "The search service rejected the API key (status 401). Check TAVILY_API_KEY."
    if response.status_code != 200:
        return f"The search service refused the request (status {response.status_code})."
```

**What this block does:** it separates "the server answered, but said no"
from "it worked", and names the most common cause — a bad key — specifically.

**Line by line:**

- `response.status_code` is the HTTP **status code**: `200` means success,
  `401` means "unauthorised", `429` means "too many requests", and so on.
- `401` is checked first and gets its own message naming the exact variable
  to fix. A person reading the trace sees what to do.
- `!= 200` catches every other failure and includes the number.

**Why it is written this way:** `requests` does not raise on a `401` or
`500`. The request "succeeded" at the network level, so the `except` in 2.3d
never fires. Without these checks, the code would try to read results out of
an error page.

### 2.3f Turning results into text

```python
    results = response.json().get("results", [])
    if not results:
        return "No results were found for that search. Say so rather than guessing."

    lines = []
    for number, item in enumerate(results, start=1):
        summary = (item.get("content") or "").strip().replace("\n", " ")[:300]
        lines.append(f"{number}. {item.get('title', 'No title')}\n   {item.get('url', '')}\n   {summary}")
    return "\n\n".join(lines)
```

**What this block does:** it reads Tavily's reply, says so in words if there
were no results, and otherwise builds a short numbered list — title, link and
a trimmed summary — for the model to read.

**Line by line:**

- `response.json()` parses the reply body from JSON into a Python dictionary.
- `.get("results", [])` reads the `"results"` key, or gives `[]` if it is
  missing. `data["results"]` would crash with a `KeyError` instead.
- `if not results:` — an empty list is falsy, so this catches "no results".
  The returned sentence tells the model an empty result is a real answer.
- `enumerate(results, start=1)` gives pairs of (count, item): `(1, first)`,
  `(2, second)` and so on. `start=1` makes the list read 1, 2, 3 rather than
  0, 1, 2.
- `item.get("content") or ""` — if `content` is missing *or* `None`, `or`
  falls back to `""`. A default in `.get("content", "")` alone would not
  cover an explicit `None`.
- `.strip()` removes spaces at both ends. `.replace("\n", " ")` flattens line
  breaks. `[:300]` is a slice that keeps at most the first 300 characters.
- `item.get('title', 'No title')` fills a gap rather than crashing.
- `"\n\n".join(lines)` joins the entries with a blank line between each.

**Why it is written this way:** everything returned here goes into the
model's context, and you pay for it by the token. Five results cut to 300
characters each keeps a search to a few hundred words, not a few pages.

One small gap: if Tavily ever returned a `200` whose body is not JSON,
`response.json()` would raise. The SDK would catch that and send its generic
"Please try again" message.

---

## 2.4 Tool 2 — `calculator`

**What this whole tool is for:** it does the arithmetic the model is bad at,
safely — accepting only plain numbers and operators, never arbitrary code.

### 2.4a The signature and docstring

```python
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
    ...
    """
```

**What this block does:** it tells the model to use this for *every*
calculation, and tells it exactly which characters it may send, so it gets
the input right the first time.

**Line by line:**

- "including simple ones" closes the loophole where the model decides
  `12 * 3` is easy enough to do itself.
- "Models are unreliable at arithmetic" gives the model the *reason*, which
  makes it more likely to follow the rule.
- The `Args:` text lists what is allowed and not allowed. The model sees
  this, so it writes `850 * 133.4` rather than `$850 × 133.4`.

### 2.4b Cleaning and the size guard

```python
    cleaned = expression.strip().replace(",", "")

    allowed = set("0123456789+-*/(). ")
    # Block ** (powers): something like 9**9**9 is so large that the
    # program would freeze trying to calculate it. Also cap the length.
    if "**" in cleaned or len(cleaned) > 100:
        return "That expression is not allowed. Use only + - * / ( ) and keep it short."
```

**What this block does:** it tidies the input, then rejects anything that
could take forever to compute — powers, and very long expressions.

**Line by line:**

- `.strip()` removes surrounding spaces. `.replace(",", "")` turns
  `"1,250 * 3"` into `"1250 * 3"`, so thousands separators do not break it.
- `set("0123456789+-*/(). ")` turns a string into a **set** — a collection of
  unique characters, fast to check against. This is the **whitelist**, used
  in 2.4c.
- `"**" in cleaned` checks for Python's power operator. Every character in
  `**` is on the whitelist, so the whitelist alone would let it through.
- `len(cleaned) > 100` caps the length.

**Why it is written this way:** `9**9**9` is made only of allowed characters,
but it has hundreds of millions of digits. Python would try to compute it,
and the agent would freeze. This is a **resource** check, separate from the
**character** check that follows.

### 2.4c The whitelist check

```python
    if not cleaned or not set(cleaned).issubset(allowed):
        return (
            "That is not a valid maths expression. "
            "Send only numbers and the symbols + - * / ( ) ."
        )
```

**What this block does:** it is the security gate. Before any of the text is
executed, it checks that every single character is one of a small permitted
set — rejecting anything else outright.

**Line by line:**

- `not cleaned` rejects an empty string.
- `set(cleaned)` is the set of characters actually used.
  `set("2 * 3")` is `{"2", " ", "*", "3"}`.
- `.issubset(allowed)` is true only if every one of them is in `allowed`.
  `"2 * 3"` passes. `"__import__('os')"` fails at the first `_`.
- `or` means either failure returns the same message, which says what *is*
  allowed so the model can fix it.

**Why it is written this way:** a **whitelist** (allow only these) is safer
than a **blacklist** (block these). A blacklist has to predict every
dangerous input and misses the one you did not think of. A whitelist of
digits and operators cannot even spell a function name.

### 2.4d Evaluating the expression

```python
    try:
        result = eval(cleaned, {"__builtins__": {}}, {})
    except Exception as error:
        return f"Could not calculate that: {error}"
```

**What this block does:** it has Python compute the expression, and turns any
maths error — dividing by zero, unmatched brackets — into a sentence the
model can act on.

**Line by line:**

- `eval(text)` runs a string as a Python expression and returns the result.
  `eval("2 * 3")` gives `6`.
- The second argument, `{"__builtins__": {}}`, gives the expression an empty
  set of built-in functions, so names like `open` or `print` do not exist.
- The third argument, `{}`, gives it no local variables.
- `except Exception as error:` catches any ordinary error. `"1/0"` becomes
  `"Could not calculate that: division by zero"`, and `"(2+3"` becomes a
  syntax-error message.

**Why it is written this way:** `eval` on untrusted input is normally
dangerous — it will run any Python it is given. What makes it safe **here**
is 2.4c, not the empty `__builtins__`. The whitelist means the text can only
ever contain digits, `.`, spaces, brackets and `+ - * /`, which cannot form a
function call or a name. Emptying `__builtins__` on its own is a weak
barrier, and it is known to be escapable. In production, use a proper
expression parser — for example Python's `ast` module walking only number and
operator nodes — or a library such as `simpleeval`.

### 2.4e Checking and rounding the result

```python
    if not isinstance(result, (int, float)):
        return "That expression did not produce a number."

    return str(round(float(result), 2))
```

**What this block does:** it makes sure the answer is really a number, then
returns it rounded to two decimal places, as text.

**Line by line:**

- `isinstance(result, (int, float))` is true if `result` is a whole number or
  a decimal. The **tuple** `(int, float)` means "either of these".
- An expression like `"()"` passes the whitelist but evaluates to an empty
  tuple, not a number. This line catches it.
- `float(result)` turns an `int` into a decimal. `round(..., 2)` rounds to two
  places: `round(113390.0, 2)` gives `113390.0`. `str(...)` turns it into text,
  because tools return strings.

---

## 2.5 Tool 3 — `send_to_discord`

**What this whole tool is for:** it posts a short message to a Discord
channel through a webhook — the one tool that acts on the outside world
rather than just reading from it.

### 2.5a The signature and docstring

```python
@function_tool
def send_to_discord(message: str) -> str:
    """Send a short message to the team's Discord channel.

    Use this ONLY when the user explicitly asks you to send, post, share or
    notify. Do NOT use it to show the user their answer — simply reply
    normally for that.
    ...
    """
```

**What this block does:** it tells the model this tool is off-limits unless
the user asks — because, unlike the other two, it has a **side effect**: a
real message appears in front of real people.

**Line by line:**

- "ONLY when the user explicitly asks" lists the trigger words — send, post,
  share, notify — so the model can spot them.
- "Do NOT use it to show the user their answer" blocks the most likely
  mistake: treating "send" as the way to reply.
- `message: str` with "Keep it under 200 characters" in `Args:` keeps posts
  short. Nothing in the code enforces that limit; it is a request to the model.

### 2.5b Checking for the webhook

```python
    webhook = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook:
        return (
            "No Discord webhook is configured, so nothing was sent. "
            "Tell the user the message could not be delivered."
        )
```

**What this block does:** if there is no webhook address, it sends nothing
and tells the model to be honest about that, rather than claim it posted.

**Line by line:**

- `os.getenv("DISCORD_WEBHOOK_URL")` reads the address, or `None`.
- `DISCORD_WEBHOOK_URL=` left blank in `.env` gives `""`, which is falsy, so
  it is treated as missing too.
- The message spells out "nothing was sent" so the model cannot mistake it
  for success.

**Why it is written this way:** this variable is optional, so a missing
value is the normal case, not an error. The webhook URL is itself a secret —
anyone who has it can post to your channel — which is why it lives in `.env`
alongside the API keys.

### 2.5c Posting and checking the reply

```python
    try:
        response = requests.post(webhook, json={"content": message}, timeout=10)
    except requests.RequestException as error:
        return f"Could not reach Discord: {error}"

    if response.status_code not in (200, 204):
        return f"Discord refused the message (status {response.status_code})."

    return "sent"
```

**What this block does:** it posts the message with a time limit, reports any
failure in words, and returns the single word `"sent"` only when Discord
confirms it.

**Line by line:**

- `json={"content": message}` is the minimum body a Discord webhook accepts:
  the text of the message under the key `content`.
- `timeout=10` — the same protection as 2.3d.
- `not in (200, 204)` — Discord replies `204 No Content` on success (or `200`
  if you ask it to return the message). Anything else is a refusal, such as
  `404` for a deleted webhook.
- `return "sent"` is short on purpose. It is unambiguous, and it costs almost
  nothing in tokens.

**Why it is written this way:** the success message is only returned after
the status check. Report success before checking, and the agent will tell the
user "posted!" for a message that never arrived.

---

# Part 3 — the patterns worth taking away

1. **The text is the interface.** The model never sees your code — only
   `INSTRUCTIONS`, each tool's name, its docstring above `Args:`, and its
   `Args:` lines. Rewrite a docstring and you change the agent's behaviour
   without changing a single line of logic.

2. **Tools return words, never silence and never exceptions.** Every failure
   path in `tools.py` returns a sentence, from "No Tavily API key is
   configured" to "Could not reach Discord". A raised error becomes the SDK's
   generic "Please try again", and an empty string looks like failure — both
   invite the model to retry.

3. **Put the instruction where the model will read it.** "Do not guess an
   answer" and "Say so rather than guessing" sit inside the returned strings
   (2.3c, 2.3f), not only in the `Returns:` section — which the SDK drops.

4. **Every external call has a timeout.** `timeout=15` for search and
   `timeout=10` for Discord (2.3d, 2.5c). `requests` waits forever by
   default, and a frozen tool call is one that `max_turns` cannot stop.

5. **Every agent has a limit.** `max_turns=10` in `ask` (1.6b) caps how many
   paid model calls one question can make, and the `except` turns hitting
   the cap into a plain message.

6. **Whitelist, do not blacklist.** The calculator decides what is *allowed*
   (`set("0123456789+-*/(). ")`) instead of guessing what is dangerous
   (2.4c). That one line is what makes the `eval` below it safe here.

7. **Secrets live in the environment.** Every key and the webhook come from
   `os.getenv`, loaded from `.env` by `load_dotenv()` (1.3). The code can be
   shared and committed; the file with the keys stays on your machine.

8. **Fail fast, at the edge.** The `__main__` guard (1.8) checks for the
   OpenAI key before anything runs and exits with a clear sentence and code
   `1`, instead of letting a stack trace appear halfway through a paid run.
