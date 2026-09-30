# 4. Reading the trace

## Why this matters more than anything else

On Day 19 you learned the debugging skill of this whole course:

> Reading the trace is the difference between someone who can debug agents
> and someone who guesses.

When people move from a visual tool to code, this is usually what they lose —
and then they wonder why debugging suddenly became hard.

You do not lose it here. The SDK records every run automatically: which model
was called, which tools were used, with what arguments, and what came back.

**Read the trace after every run.** Not "check whether it worked." Read what
it actually did.

---

## Where the trace is

Tracing is on by default. Each run is uploaded to OpenAI using the same
`OPENAI_API_KEY`, and you read it at:

    platform.openai.com/traces

Each run shows up as a trace named "Agent workflow". Open it and you get one
row per step: the model call, each tool call with its arguments, and each
tool's result.

To switch uploading off — for example when the questions contain customer
data — add this to `.env`:

    OPENAI_AGENTS_DISABLE_TRACING=1

If you use a non-OpenAI model (the Ollama setup in `01-setup-guide.md`), the
upload has nowhere useful to go. Use the local method below instead.

---

## The order to check things

Work through these in order. Do not skip ahead.

| Step | Question | Where the bug usually is |
|---|---|---|
| 1 | Did the input arrive as you expected? | |
| 2 | **What exact text went to the model?** | ← most bugs |
| 3 | What did the model output, before parsing? | |
| 4 | What arguments did it pass to the tool? | |
| 5 | **What did the tool actually return?** | ← most other bugs |

Step 2 is the one people skip. They read what they *think* they wrote, not
what was assembled and sent.

---

## Seeing it locally, without any setup

If you just want to watch the steps while learning, print the items:

    result = Runner.run_sync(agent, question)

    for item in result.new_items:
        print(type(item).__name__, "→", item)

That gives you the sequence of what happened: the tool calls, their
arguments, and their results.

---

## The three questions

When something goes wrong, answer these three before changing anything:

1. **What exactly did you send it?**
2. **What exactly did it choose?**
3. **What exactly came back?**

Most of the time you cannot answer all three — and finding out solves the
problem before you have changed a line.
