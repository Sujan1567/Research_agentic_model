"""
Example questions to try.
=========================

Run this to work through the demo sequence in order. Each question shows
something the one before it did not.

    python run_examples.py          run all of them
    python run_examples.py 2        run just number 2
"""

import sys
from research_assistant import ask

EXAMPLES = [
    (
        "Warm-up — one tool",
        "What is the population of Kathmandu?",
        "One search, one answer. Confirms the search tool and your key work.",
    ),
    (
        "The main demo — two tools, in order",
        "Find the current USD to NPR rate and tell me what 850 dollars is worth.",
        "It must search FIRST to get the rate, then feed that number into the "
        "calculator. Nobody told it to do that. Stop here and read the trace.",
    ),
    (
        "Choosing NOT to use a tool",
        "What is an exchange rate?",
        "It answers from its own knowledge. No tool call. Choosing not to "
        "use a tool is also a decision, and it is the cheap one.",
    ),
    (
        "Being honest about a gap",
        "How much profit did Himalayan Java Coffee make last year?",
        "A small private company rarely publishes this. A good agent says it "
        "could not find it. A bad one invents a number.",
    ),
    (
        "Two numbers, then arithmetic",
        "What is the population of Pokhara, and what percentage of Nepal's "
        "population is that?",
        "Two facts to find, then one calculation. Watch how many searches it "
        "decides to make.",
    ),
    (
        "Three tools in one sentence",
        "Convert 200 euros to pounds and post the answer to Discord.",
        "Search, calculate, send. Needs DISCORD_WEBHOOK_URL set.",
    ),
]


def run(index: int) -> None:
    title, question, note = EXAMPLES[index]
    print("\n" + "=" * 72)
    print(f"{index + 1}.  {title}")
    print("=" * 72)
    print(f"\nQ: {question}\n")
    print(f"A: {ask(question)}\n")
    print(f"[ {note} ]")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(int(sys.argv[1]) - 1)
    else:
        for i in range(len(EXAMPLES)):
            run(i)
