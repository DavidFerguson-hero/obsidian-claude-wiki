#!/usr/bin/env python3
"""Pick a truly random note from 10 Notes/ — for the daily inspiration prompt.

    python3 random_note.py              (Windows: py random_note.py)
    python3 random_note.py --days 60    # skip notes picked in the last 60 days (default)

Prints the note's path relative to the vault, and records the pick in
`00 Inbox/_inspiration-log.md` so the same note doesn't come back too soon.
Index pages (`+…`) are never picked; example notes only until you have real ones.

The randomness is deliberate: an agent asked to "pick an interesting note"
gravitates to the same handful. This script makes the choice instead.
"""
import argparse
import datetime as dt
import random
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VAULT = Path(__file__).resolve().parent
NOTES = VAULT / "10 Notes"
LOG = VAULT / "00 Inbox" / "_inspiration-log.md"


def recent_picks(days):
    if not LOG.exists():
        return set()
    cutoff = dt.date.today() - dt.timedelta(days=days)
    picked = set()
    for m in re.finditer(r"^- (\d{4}-\d{2}-\d{2}) · \[\[(.+?)\]\]", LOG.read_text(encoding="utf-8"), flags=re.M):
        if dt.date.fromisoformat(m.group(1)) >= cutoff:
            picked.add(m.group(2))
    return picked


def is_example(p):
    head = p.read_text(encoding="utf-8", errors="replace")[:1500]
    return bool(re.search(r'tags:.*["\s\[]example["\s,\]]', head))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=60, help="don't repeat a note picked within this many days")
    ap.add_argument("--no-log", action="store_true", help="pick without recording it")
    a = ap.parse_args()

    if not NOTES.is_dir():
        print("No `10 Notes/` folder found next to this script.")
        return 1
    every = [p for p in NOTES.rglob("*.md") if not p.name.startswith("+")]
    notes = [p for p in every if not is_example(p)] or every   # examples only until real notes exist
    if not notes:
        print("No notes to pick from yet.")
        return 1
    recent = recent_picks(a.days)
    fresh = [p for p in notes if p.stem not in recent] or notes   # if all were used recently, allow repeats
    pick = random.SystemRandom().choice(fresh)

    if not a.no_log:
        if not LOG.exists():
            LOG.write_text("---\ntitle: \"Inspiration log\"\ntype: log\n---\n\n# Inspiration log\n\n"
                           "Written by `random_note.py`. Newest at the bottom.\n\n", encoding="utf-8")
        with LOG.open("a", encoding="utf-8") as f:
            f.write(f"- {dt.date.today()} · [[{pick.stem}]]\n")

    print(pick.relative_to(VAULT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
