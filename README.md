# Joke Explainer

Fetches a random joke and sends it to Claude for an explanation of why it's funny.

Written using only the Python standard library (`urllib`, `json`), no pip install. Temporarily on an old machine, kept dependency-free to avoid install problems.

## Setup

```bash
export ANTHROPIC_API_KEY="YOUR_KEY"
```

Get a key from console.anthropic.com. Keep it as an environment variable (NOT hardcoded in the script).

## Usage

```bash
python3 joke_explainer.py
```

Example output:

```
Why did the scarecrow win an award?
Because he was outstanding in his field.

Why it works: The joke hinges on the double meaning of "outstanding," literally standing out in a farm field, and figuratively being exceptional. The pun collapses both senses into one word for the punchline.
```

## macOS note

python.org installers have supported macOS 10.13 and newer since Python 3.12.6. Check what's installed with `python3 --version`.

## Error handling

Network calls can fail for ordinary reasons: no internet connection, a bad API key, a rate limit. The script catches these and prints a clear message instead of crashing with a raw traceback.

There is one detail specific to `urllib`. When `HTTPError` is raised, its default message is generic, something like "HTTP Error 401: Unauthorized." The actual reason (bad key, rate limit, etc.) is in the response body, not in that default message. `e.read()` reads the body so the script can show the real error instead of the generic one.

## Differences from Repo Analyzer

- Uses `urllib` instead of `requests`. No pip installs for this project, so requests are built manually with `Request` objects, and the JSON payload has to be encoded to bytes by hand.
- This is a POST request with a JSON body. Repo Analyzer only made GET requests.
- Calling an LLM API means building a messages payload and reading the content blocks back out of the response.
- Reads the API key from an environment variable with `os.environ.get()` instead of hardcoding it.
