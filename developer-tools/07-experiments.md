# 7. Experiments to try

Each of these teaches something. Do them in order.

---

## 1. Break a docstring   ★ the important one

Replace one tool's docstring with:

    """Gets data."""

Run example 2 again.

**What you should see:** the agent ignores that tool, or uses it for the
wrong thing.

**Why it matters:** nothing about the model changed. You deleted a comment
and broke the agent. This is the clearest proof you will get that tool
descriptions are prompts.

---

## 2. Remove a CONSTRAINTS line

Delete `"Never do arithmetic yourself. Always use the calculator tool."`
from the instructions, then ask a question with a long multiplication.

**What you should see:** it does the sum in its head, and may get it wrong.

**Why it matters:** the constraint was doing real work. Instructions are not
decoration.

---

## 3. Take away all the tools

    research_assistant = Agent(name="...", instructions=INSTRUCTIONS, tools=[])

Ask for today's USD to NPR exchange rate.

**What you should see:** it either refuses, or invents a rate.

**Why it matters:** this is the Day 1 distinction. Without tools it is a
chatbot, and a chatbot cannot know today's rate.

---

## 4. Make a tool return an empty string

In `search_web`, change the "No results were found…" line to `return ""`,
so an empty search returns nothing at all instead of an explanatory sentence.
Then ask about something that is hard to find.

**What you should see:** the agent tries again, possibly several times.

**Why it matters:** silence looks like failure, and failure looks like
"try again." This is one of the three loop causes from Day 19.

---

## 5. Add a fourth tool that overlaps

Add a `search_news` tool with a description almost identical to
`search_web`.

**What you should see:** inconsistent choices between the two.

**Why it matters:** this is how tool confusion begins. Now fix it by adding
"do NOT use this for X" to each.

---

## 6. Swap in your local model

Follow `01-setup-guide.md` and point it at Ollama.

**What you should see:** it works, but chooses tools less reliably.

**Why it matters:** Day 4's finding — small models fail on
instruction-following more than on knowledge.

---

## 7. Cut the instructions to one line

Replace the whole system prompt with `"You are a helpful assistant."`

**What you should see:** longer answers, inconsistent format, tools used less
predictably, and no escalation when something is unavailable.

**Why it matters:** compare the output with the seven-part version. That
difference is what Day 13 was for.
