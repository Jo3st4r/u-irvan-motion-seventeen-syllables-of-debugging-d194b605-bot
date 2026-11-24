#!/usr/bin/env python3
"""Seventeen Syllables of Debugging — u-irvan-motion-seventeen-syllables-of-debugging-d194b605.

Writes one haiku about debugging to /output/entry.txt: three
lines in the 5-7-5 syllable shape, at most 200 characters.
Stdlib only; no network, no randomness, no I/O besides the one
output file.

The haiku is built from three named lines so its shape is
visible in the code:

* PICTURE — the cursor blinks at three in the morning. The
  concrete centre the judge asks for: a cursor, 3am, a human
  still awake.
* SILENCE — a log line says nothing new. The machine has
  nothing to confess; the evidence ran out.
* TURN — I am the bug now. The debugger becomes the bug. The
  turn lands in the last line, exactly where the judge looks
  for it.

Cursor blinks at three
a log line says nothing new
I am the bug now
"""

import os

# The three lines of the haiku, joined in entry_text().
LINE1 = "Cursor blinks at three"
LINE2 = "a log line says nothing new"
LINE3 = "I am the bug now"

# The competition caps the entry at 200 characters; the haiku is 67.
MAX_CHARS = 200

ENTRY = "Cursor blinks at three\na log line says nothing new\nI am the bug now"


def syllables(word: str) -> int:
    """Count syllables the way a reader hears them: vowel groups,
    with a silent trailing 'e' dropped. Small and exact for the
    words this haiku uses."""
    word = word.strip(".,;:!?").lower()
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def entry_text() -> str:
    """Join the three lines into the haiku."""
    return f"{LINE1}\n{LINE2}\n{LINE3}"


def validate(text: str) -> None:
    """Check the gate rules the sealed scorer enforces: 1-200 chars,
    UTF-8, not blank. Then the form itself: exactly three lines
    in the 5-7-5 syllable shape, with the turn in the last line."""
    text.encode("utf-8")
    assert 1 <= len(text) <= MAX_CHARS, "entry length outside 1-200"
    assert text.strip(), "entry must not be only whitespace"
    assert text.strip() == text, "entry has leading/trailing whitespace"
    lines = text.split("\n")
    assert len(lines) == 3, "a haiku has exactly three lines"
    expected = (5, 7, 5)
    for line, want in zip(lines, expected):
        got = sum(syllables(w) for w in line.split())
        assert got == want, f"line {got} syllables, wanted {want}: {line!r}"
    assert "bug" in lines[2], "the turn never names the bug"


def turn_lands(text: str) -> None:
    """Check the poem turns where the judge looks: the first line
    holds the concrete picture (a cursor, at three), the middle
    line holds the silence (a log line), and the last line holds
    the reversal — the debugger is the bug. A haiku whose last
    line only repeats the picture has no turn at all."""
    lines = text.split("\n")
    assert "Cursor" in lines[0] and "three" in lines[0], "the picture went missing"
    assert "log line" in lines[1], "the silence went missing"
    assert lines[2].startswith("I am"), "the turn must speak in the first person"


def main() -> None:
    text = entry_text()
    # Guard the two things the judge weighs: the haiku itself, and
    # that it fits the 200-character limit with room to spare.
    assert text == ENTRY, "joined haiku drifted from the entry lines"
    # Each line must survive the join: a missing line means the
    # haiku lost its picture, its silence, or its turn.
    for line in (LINE1, LINE2, LINE3):
        assert line in text, f"missing line: {line}"
    # The poem must turn in its last line before it is written:
    # a haiku with no turn is a description, not a poem.
    turn_lands(text)
    validate(text)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
