"""The Painfully Honest Out-of-Office — make.fun entry.

Writes one brutally honest but still polite out-of-office auto-reply
(at most 200 characters) to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).

Pure standard library only.
"""

import os

LINE = (
    "I'm on leave and won't be checking email \u2014 my inbox will "
    "still be here when I return, and so, unfortunately, will I."
)

MAX_CHARS = 200


def validate(text):
    """Enforce the RULES.txt gate: UTF-8, 1-200 chars, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 200-char limit" % len(text))
    # Control characters would break the single-line UTF-8 gate, so
    # reject them explicitly rather than letting them slip into entry.txt.
    if any(ord(c) < 0x20 or ord(c) == 0x7F for c in text):
        raise ValueError("entry contains a control character")
    text.encode("utf-8")


def main():
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    validate(written)
    if written != LINE:
        raise ValueError("written entry does not match the line")


if __name__ == "__main__":
    main()
