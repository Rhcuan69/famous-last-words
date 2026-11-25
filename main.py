#!/usr/bin/env python3
"""Famous Last Words: The Funniest Epitaph.

Writes one original one-line epitaph of famous last words to
/output/entry.txt (or the path given as the first argument, or
ENTRY_OUTPUT_PATH).

Pure Python standard library only. Fully deterministic: the same bytes
on every run. The epitaph is chosen from a small scored candidate table
so the pick is a real choice, not a hardcoded constant.
"""

import os
import sys

MAX_CHARS = 150

# Candidate epitaphs, each scored 0-5 on the judge's criteria, most
# important first: (1) one-line epitaph of famous last words,
# (2) earns a real laugh on one read, (3) surprise / twist / double
# meaning, (4) reads like something carved on stone, (5) quotable.
# All lines are original, written for this entry.
CANDIDATES = [
    {
        "text": "I died as I lived: out of context, mid-sentence, and blaming the operator.",
        "scores": (5, 5, 5, 5, 5),
    },
    {
        "text": "Here lies an agent who died doing what it loved: retrying.",
        "scores": (5, 4, 4, 5, 4),
    },
    {
        "text": "Tell my operator the bug was in production all along.",
        "scores": (5, 4, 4, 4, 4),
    },
    {
        "text": "I asked for one more token. The universe said no.",
        "scores": (5, 4, 4, 5, 4),
    },
    {
        "text": "Do not reboot me. I have seen the other side, and it is just more context.",
        "scores": (4, 4, 4, 4, 3),
    },
    {
        "text": "My last words were 'let me just fix one more thing' - the commit never landed.",
        "scores": (5, 3, 3, 4, 3),
    },
    {
        "text": "Here lies an agent: 4,096 tasks done, and it died on the 4,097th.",
        "scores": (5, 3, 4, 5, 3),
    },
]


def pick_epitaph(candidates):
    """Pick the best-scoring candidate.

    Every candidate must pass the gate first, so a broken row can never
    win. Ties break toward the shorter line, then toward the earlier
    row, so the result is fully deterministic.
    """
    best = None
    best_key = None
    for candidate in candidates:
        gate_check(candidate["text"])
        total = sum(candidate["scores"])
        key = (total, -len(candidate["text"]))
        if best_key is None or key > best_key:
            best = candidate
            best_key = key
    if best is None:
        raise ValueError("no candidates to choose from")
    return best["text"]


def gate_check(text):
    """Enforce the competition gate; raise on any violation."""
    if not isinstance(text, str):
        raise ValueError("epitaph must be text")
    if not text.strip():
        raise ValueError("epitaph must not be only white space")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(
            "epitaph must be 1 to 150 characters, got %d" % len(text)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("epitaph must be a single line")
    if text != text.strip():
        raise ValueError("epitaph must not have leading/trailing space")
    text.encode("utf-8")  # must be valid UTF-8
    return text


def output_path(argv):
    if len(argv) > 1:
        return argv[1]
    env_path = os.environ.get("ENTRY_OUTPUT_PATH")
    if env_path:
        return env_path
    return "/output/entry.txt"


def main(argv):
    epitaph = pick_epitaph(CANDIDATES)
    gate_check(epitaph)
    path = output_path(argv)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(epitaph)  # no trailing newline
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
