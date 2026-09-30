# 2. SDK reference

## What this framework is

A thin wrapper around the agent loop. It has a small number of pieces and
then gets out of your way. Of the four frameworks in this course, it has the
least ceremony — you can have something running in about fifteen lines.

It began as an experimental project called **Swarm**. If you find older
tutorials mentioning Swarm, that is the same lineage.

---

## The six pieces

| Piece | What it is | Where you saw it in n8n |
|---|---|---|
| **Agent** | A model plus instructions, tools and handoffs | The AI Agent node |
| **Runner** | Runs the loop until there is a final answer | n8n ran the loop for you |
| **Tools** | Python functions the agent may call | The tool sub-nodes |
| **Handoffs** | Passing control to a different agent | New — Day 22 |
| **Guardrails** | Checks on input and output | New — Day 22 |
| **Sessions** | Memory that survives between turns | The Memory sub-node |

---

## Agent — the options

    Agent(
        name="Research Assistant",     # required. Used in traces and handoffs
        instructions=INSTRUCTIONS,     # the system prompt
        tools=[tool_a, tool_b],        # list of @function_tool functions
        model="gpt-4o-mini",           # optional. Defaults to the SDK default
        handoffs=[other_agent],        # optional. Day 22
        output_type=SomeModel,         # optional. Forces a structured answer
    )

### `instructions`

This is where the seven-part structure from Day 13 goes: ROLE, OBJECTIVE,
TOOLS, PROCESS, CONSTRAINTS, ESCALATION, OUTPUT FORMAT.

It can also be a function, if you need the instructions to change per run —
for example inserting the customer's name or today's date.

### `model`

Set it per agent. This is Day 3's tiering advice in one line: a cheap model
for routing and extraction, a better one for the step that needs judgement.

### `output_type`

Give it a Pydantic model and the agent must return that shape. This is
Day 10's **Type** letter. Use it whenever your code has to read the answer
rather than a person.

---

## Runner — two ways to run

| Call | Behaviour | Use it |
|---|---|---|
| `Runner.run_sync(agent, "question")` | Blocks until finished | While learning |
| `await Runner.run(agent, "question")` | Asynchronous | In real applications |
| `Runner.run_streamed(...)` | Streams tokens as they arrive | When a person is waiting |

The result object gives you:

    result.final_output        the answer
    result.new_items           what happened during the run

---

## What `Runner.run` actually does

    1.  Send the model your instructions, the conversation, and the tools
    2.  The model replies — a final answer, or a tool call
    3.  If final answer  →  stop and return it
    4.  If tool call     →  run the function, add the result
    5.  Go back to step 1

That is the Day 1 loop, and the same loop the n8n AI Agent node ran for you.

**You still are not writing the loop. The framework writes it.**
That is what a framework is for.

---

## Two features you will need later

| Feature | What it gives you | When |
|---|---|---|
| **MCP support** | Connect to any MCP server as a tool source | Day 8's protocol, in code |
| **Human in the loop** | Pause and ask a person before continuing | Lesson 8, and your capstone |

You do not need either today. Knowing they exist stops you building them
yourself later.
