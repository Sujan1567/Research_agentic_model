# 5. Troubleshooting

## Setup problems

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: agents` | Not installed, or wrong environment | Activate `.venv`, then `pip install -r requirements.txt` |
| `No OPENAI_API_KEY found` | `.env` missing or misnamed | It must be `.env`, not `env` or `.env.txt` |
| Key is set but still rejected | `load_dotenv()` not called, or key has a typo | Check for spaces or quotes around the key in `.env` |
| `python: command not found` | Python not on PATH | Try `python3` |
| Installed but import fails | Wrong virtual environment active | Check your prompt starts with `(.venv)` |

---

## Agent behaviour problems

**These are the ones that matter, and almost all of them are text problems.**

| What you see | What is actually wrong | Fix |
|---|---|---|
| It ignores a tool completely | The docstring does not say **when** to use it | Rewrite it: when to use, when not to |
| It calls a tool with wrong values | The arguments are not described | Describe each one, with an example value |
| It calls the same tool over and over | It cannot tell it succeeded | Make the tool return words, not an empty string |
| It answers without using tools | Nothing told it that it must | Add a CONSTRAINTS line: "never guess a rate" |
| It invents a number | No rule about what to do when unknown | Day 10's null rule, in the instructions |
| Good once, wrong the next time | Normal variation | Test with a golden set, not one run |
| It uses the wrong tool of two similar ones | The two descriptions overlap | Add "do NOT use this for X" to both |

Notice the pattern. Almost every row is fixed by **editing a docstring or the
instructions** — not by switching to a bigger model.

---

## Tool problems

| Symptom | Fix |
|---|---|
| `requests.exceptions.Timeout` | The API is slow. The timeout is working correctly |
| Search says "No Tavily API key is configured" | Add `TAVILY_API_KEY` to your `.env` file |
| Search says the key was rejected (401) | The Tavily key is wrong or expired. Copy it again from tavily.com |
| Search says "No results were found" | That is a real answer. The agent should say so, not guess |
| Discord says nothing was sent | `DISCORD_WEBHOOK_URL` is not set in `.env` |
| Calculator refuses an expression | It only accepts digits and `+ - * / ( )`, with no `**` and under 100 characters |
| "The agent stopped after 10 steps" | The step limit worked. Read the trace to see why it kept going |

---

## The first three things to check, always

1. Is your virtual environment active?
2. Is the model name spelled exactly right?
3. Read the docstring of the tool that misbehaved.

That is most of it.
