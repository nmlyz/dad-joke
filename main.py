#!/usr/bin/env python3
"""dad-joke: write one dad joke to /output/entry.txt.

The joke is a dinner-table dad joke: a father asks his son to pass the
butter, and the son refuses, because he does not spread gossip at the
dinner table. The pun turns on "spread" (butter / gossip), lands on the
first read, and the punchline arrives at the end.

Standard library only, no network. Deterministic: the same bytes on every run.
"""

import os
import sys

# The joke is built from two clauses, one per beat, so each beat can be
# checked on its own: the father asking for the butter, then the son's
# refusal that turns "spread" from butter into gossip.
CLAUSES = (
    "I asked my son to pass the butter,",
    "and he said, 'I don't spread gossip at the dinner table.'",
)

LINE = " ".join(CLAUSES)

MIN_LEN = 1
MAX_LEN = 200


def problems(text: str) -> list:
    """Return every gate violation for the entry text (empty means valid)."""
    found = []
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        found.append(f"entry is {len(text)} code points, must be {MIN_LEN}-{MAX_LEN}")
    stripped = text.strip()
    if not stripped:
        found.append("entry must not be only white space")
    if text != stripped:
        found.append("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    if "  " in text:
        found.append("entry must not contain a double space")
    if not (stripped.endswith(".") or stripped.endswith(".'")):
        found.append("entry must end as one sentence")
    return found


def main() -> int:
    if len(CLAUSES) != 2:
        print("joke must be built from exactly two clauses", file=sys.stderr)
        return 1
    text = LINE
    bad = problems(text)
    if bad:
        for item in bad:
            print(item, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # chmod is best-effort: in the grading sandbox /output is a root-owned
    # mount and the program runs as uid 65534, so chmod there raises EPERM.
    # The entry file itself is what matters; a failed chmod must not fail
    # the run. (The output directory itself is never chmodded or removed.)
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    # Read the file back as bytes and confirm they match the joke exactly.
    with open(path, "rb") as f:
        if f.read() != text.encode("utf-8"):
            print("entry.txt does not match the dad joke", file=sys.stderr)
            return 1
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
