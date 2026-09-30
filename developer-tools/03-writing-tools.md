# 3. Writing tools

## The one thing to understand

A tool is an ordinary Python function with one decorator on it.

    from agents import function_tool

    @function_tool
    def search_web(query: str) -> str:
        """Search the web for current information. ..."""
        ...

The framework reads your function and builds the tool definition from it:

| What the model sees | Where it comes from |
|---|---|
| The tool's name | Your function name |
| What it does and when to use it | **Your docstring — the text above `Args:`** |
| What arguments it takes | Your parameter names and type hints |
| What each argument means | The matching line under `Args:` |

**The model never sees your code.** Only those four things.

Note what is not in the table: the `Returns:` section. In this SDK
(checked on `openai-agents` 0.22) it is parsed and then thrown away. Check
it yourself:

    python -c "import tools; print(tools.calculator.description)"

> On Day 13 you learned that a tool description is a prompt.
> Here, your docstring **is** the prompt.

---

## Why this trips people up

Most programmers write short docstrings, or none. In normal code that is a
style issue. Here it directly breaks the agent — and it does so quietly,
because a missing tool call does not raise an error.

When a student says "the model is ignoring my tool", open the docstring
first. It is nearly always the answer.

---

## The four things a good docstring says

1. **What it does** — one line
2. **When to use it, and when NOT to** — both halves
3. **What each argument expects** — with an example value
4. **What it returns, including on failure** — especially what empty means

Put number 4 somewhere the model will actually read it. Either write it in
the text above `Args:`, or — better — make the returned string say it:
`"No results were found for that search. Say so rather than guessing."`
A `Returns:` section is still useful to the humans reading your code, but
do not rely on it to instruct the model.

---

## Weak and strong

**Weak:**

    @function_tool
    def search(q: str) -> str:
        """Searches."""

The model does not know what it searches, when to use it, or what comes back.
It will either ignore this tool or use it for everything.

**Strong:**

    @function_tool
    def search_hotels(city: str, max_price: int) -> str:
        """Search hotels by city and maximum nightly price in NPR.

        Use this for accommodation questions only.
        Do NOT use it for flights or restaurants.

        Args:
            city: city name in Nepal, e.g. "Pokhara"
            max_price: maximum price per night in NPR, e.g. 4000

        Returns:
            A list of hotels with name, price, rating and distance to the
            city centre. Returns an empty list if nothing matches — that is
            a real answer, not an error. Do not invent hotels to fill it.
        """

That `Returns:` block reads well, but remember the model will not see it.
For the model, the function must return `"No hotels matched. That is a real
answer — do not invent one."` rather than a bare `[]`.

---

## The line people forget

> Returns an empty list if nothing matches — that is a real answer, not an error.

Without that sentence, an empty result looks like a failure, so the agent
tries again. And again. That is one of the three classic loop causes from
Day 19.

**Make your tools say what happened, in words. Silence looks like failure,
and failure looks like "try again."**

---

## How many tools?

| Number | What to do |
|---|---|
| Up to about 10 | Good docstrings are enough |
| 10 to 20 | Watch for wrong choices. Tighten the descriptions |
| More than 20 | Split into separate agents, or filter before the model sees them |

Accuracy drops noticeably past roughly 15 to 20 tools in active use. Two
similar descriptions become hard to tell apart, and the model guesses.
