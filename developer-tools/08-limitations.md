# 8. Limitations

What this framework does not do well. Know these before you choose it for a
real project.

---

## No checkpointing

If the program stops halfway — a crash, a restart, a closed laptop — the work
is gone. There is no saved state to resume from.

**Why it matters:** an agent that took four minutes and cost NPR 30 has to
start again from the beginning, and you pay again.

**What to use instead:** LangGraph, Day 26.

---

## Limited control over the loop

The framework decides how the loop runs. You can set a maximum number of
turns, but you cannot easily branch, retry one step differently, or hold
state between steps in a structured way.

**What to use instead:** LangGraph, where you draw the graph yourself.

---

## No built-in persistence between runs

Sessions give you memory within a conversation. Remembering a customer next
week is something you build yourself — that is Lesson 6.

---

## Handoffs are one-way

Once an agent hands off, control moves across. There is no natural way for
the second agent to hand back partway, or for two agents to discuss
something.

**What to use instead:** the conversational pattern, Day 27.

---

## You write the integrations

There is no ready-made Google Sheets node. If you want to write to a sheet,
you write that tool and authenticate it yourself.

**What to use instead:** n8n, or n8n around the outside of this.

---

## Model behaviour is still model behaviour

No framework fixes these. They are properties of the model:

- The same question can give a different answer
- It can still invent things if your instructions allow it
- Tool selection degrades as the tool list grows
- Long contexts reduce accuracy — Day 2

---

## When this framework is the right choice

| Good fit | Poor fit |
|---|---|
| One agent, a handful of tools | Long expensive runs that must not restart |
| Getting something working quickly | Anything needing a precise human approval gate |
| Learning how the loop works | Complex branching you need to control |
| A prototype you will rewrite | Heavy integration with business apps |
