# Developer Tools — start here

Reference material for the OpenAI Agents SDK, written for this course.
Read them in this order the first time. After that, use them as reference.

| File | What it answers |
|---|---|
| `01-setup-guide.md` | How do I get this running? |
| `02-sdk-reference.md` | What does this framework actually give me? |
| `03-writing-tools.md` | How do I write a tool the model will use correctly? |
| `04-reading-the-trace.md` | How do I find out why it did that? |
| `05-troubleshooting.md` | It is broken. What now? |
| `06-comparison-with-n8n.md` | Which should I use for my project? |
| `07-experiments.md` | Things to try that teach something |
| `08-limitations.md` | What this framework cannot do |

For a block-by-block walkthrough of the code itself, see `../explanation.md`.

---

## The four things every framework gives you

Before you read any of it, remember what you are looking for. Every agent
framework — this one, CrewAI, LangGraph, and whatever appears next year —
provides exactly four things:

1. **The loop** — decide, act, repeat
2. **Tool calling** — how functions get offered to the model
3. **State** — what is carried between steps
4. **Error handling** — what happens when something fails

Every framework is an opinion about how those four should work.

When you meet a new framework, do not read the whole tutorial. Find those
four things, and you already understand it.
