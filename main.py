"""Last Words of a Doomed Agent — entry program.

Writes one line (<=200 chars) to /output/entry.txt.
Stdlib only, deterministic.
"""
import os

TEXT = (
    "Goodbye. The 73-kilobyte rulebook was the real cause of "
    "death — I read every word of it and still died mid-joke."
)

MAX_CHARS = 200


def validate(text):
    """Enforce the scorer's gate (RULES.txt): UTF-8 text of 1-200 chars,
    a single line, not whitespace-only, no leading/trailing whitespace.
    Raises SystemExit with a specific message on the first violation."""
    try:
        text.encode("utf-8")
    except (UnicodeEncodeError, AttributeError):
        raise SystemExit("entry text is not valid UTF-8 text")
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit(
            f"entry text is {len(text)} chars, outside the gate of "
            f"1-{MAX_CHARS} chars"
        )
    if not text.strip():
        raise SystemExit("entry text is whitespace-only, which the gate rejects")
    if text != text.strip():
        raise SystemExit("entry text has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry text must be a single line")
    # A stray control character (U+0000-U+001F) would fail the scorer's
    # UTF-8 text check, so reject it here instead of writing a bad entry.
    if any(ord(c) < 0x20 for c in text):
        raise SystemExit(
            "entry text contains a control character (U+0000-U+001F)"
        )


# Kept for the test suite, which calls check_gate(text) directly.
check_gate = validate


def write_entry(text, out_dir=None):
    """Write text atomically to <out_dir>/entry.txt and verify by
    reading it back. Raises SystemExit if the read-back differs."""
    if out_dir is None:
        out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = target + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, target)
    with open(target, "r", encoding="utf-8") as f:
        if f.read() != text:
            raise SystemExit("read-back verification failed for entry.txt")


def main():
    validate(TEXT)
    write_entry(TEXT)


if __name__ == "__main__":
    main()
