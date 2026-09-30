# 6. Comparison with n8n

You have now built the same agent twice. Fill this in from your own
experience, not from what you expect the answer to be.

| Question | n8n | Agents SDK |
|---|---|---|
| How long did it take to build? | | |
| How many nodes or lines? | | |
| How easy was it to see what the agent did? | | |
| How easy would it be to change one tool? | | |
| Could a non-programmer maintain it? | | |
| Could you test it automatically? | | |
| What happened when you broke it on purpose? | | |
| Which error message was more useful? | | |

---

## There is no right answer

You will need both. The point of building it twice is learning what each one
actually costs you.

**What code gives you:** version control, automatic testing, complex logic,
and not being tied to one company's product.

**What n8n gives you:** integrations already built and authenticated, speed,
visibility without adding logging, and something you can hand to a client's
non-technical staff.

---

## What professionals actually do

> Visual tools for the plumbing — triggers, integrations, delivery.
> Code for the hard logic in the middle.

A common real shape: n8n receives the webhook and sends the Slack message,
and calls a Python service in the middle where the agent logic lives.

---

## For your capstone

Answer honestly:

- If your project is three integrations and one AI step → **n8n**, and say so
- If it has branching, loops and conditions you control → **code**
- If someone non-technical maintains it after you → **n8n**
- If it must not lose work when it crashes → **code**, specifically LangGraph
- If it is most real projects → **both**

"n8n" is a perfectly good answer for a capstone. Choosing code because it
sounds more professional is the wrong reason, and it is the same mistake as
Day 5.
