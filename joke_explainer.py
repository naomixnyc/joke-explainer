"""
joke_explainer.py - fetch a random joke, ask an LLM to explain why it's funny.

Uses only Python's standard library (urllib, json) - no pip install needed.
No compiled dependencies, so there's nothing that can fail to build.

Usage:
    export ANTHROPIC_API_KEY="YOUR_KEY"
    python3 joke_explainer.py
"""

import json
import os
import sys
import urllib.request
import urllib.error

JOKE_URL = "https://official-joke-api.appspot.com/random_joke"
CLAUDE_URL = "https://api.anthropic.com/v1/messages"


def fetch_joke() -> dict:
    # urllib needs a Request object to set headers; requests does this implicitly
    req = urllib.request.Request(JOKE_URL, headers={"User-Agent": "joke-explainer-script"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())  # no auto-decode like requests' .json()


def explain_joke(setup: str, punchline: str, api_key: str) -> str:
    prompt = f"Setup: {setup}\nPunchline: {punchline}\n\nExplain why this joke works in 2-3 sentences."

    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")  # urllib wants bytes, not a dict/string

    req = urllib.request.Request(
        CLAUDE_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())

    # content is a list of blocks (text, tool_use, etc.) - grab the text ones
    return "".join(block["text"] for block in data["content"] if block["type"] == "text")


def main() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Set ANTHROPIC_API_KEY first: export ANTHROPIC_API_KEY=\"YOUR_KEY\"")
        sys.exit(1)

    try:
        joke = fetch_joke()
    except urllib.error.URLError as e:
        print(f"Error fetching joke: {e}")
        sys.exit(1)

    print(f"\n{joke['setup']}")
    print(f"{joke['punchline']}\n")

    try:
        explanation = explain_joke(joke["setup"], joke["punchline"], api_key)
    except urllib.error.HTTPError as e:
        # HTTPError body has the actual API error message (bad key, rate limit, etc.)
        print(f"Error calling Claude: {e.code} {e.read().decode()}")
        sys.exit(1)

    print(f"Why it works: {explanation}")


if __name__ == "__main__":
    main()
