#!/usr/bin/env python3
"""
Apply the attention log to note frontmatter
===========================================
Reads `Attention log.md`, and for every entry of the form

    - 2026-08-04 · [[Some signal note]] — where it was used

writes `last_used` and `used_count` into that note's frontmatter, so Dataview
and lint can see which signals have actually earned their keep.

This is the only script that writes to notes outside an ingest. It touches two
fields and nothing else — it never edits prose, and it never changes a score.

    python3 apply_attention.py            # apply
    python3 apply_attention.py --dry-run  # report only
"""

import re, sys, collections
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):   # Windows consoles default to a non-UTF-8 code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent
LOG  = next((p for p in (ROOT / "Admin" / "Attention log.md", ROOT / "Attention log.md") if p.exists()),
            ROOT / "Admin" / "Attention log.md")
NOTES = ROOT / "10 Notes"
DRY = "--dry-run" in sys.argv

ENTRY = re.compile(r"^\s*-\s*(\d{4}-\d{2}-\d{2})\s*[·|-]\s*\[\[([^\]|#]+)")


def main():
    if not LOG.exists():
        print(f"✗ {LOG.name} not found"); return 1

    text = LOG.read_text(encoding="utf-8")
    # only the Log section counts — the format example above it is not an entry
    sec = re.search(r"^##\s*Log\s*$(.*?)(?=^##\s|\Z)", text, flags=re.S | re.M)
    if not sec:
        print("  ✗ No '## Log' section found in Attention log.md"); return 1

    uses = collections.defaultdict(list)
    for line in sec.group(1).split("\n"):
        m = ENTRY.match(line)
        if m and "example entry" not in line:
            uses[m.group(2).strip()].append(m.group(1))
    if not uses:
        print("  No real entries yet — add a line to the Log section of Attention log.md")
        return 0

    index = {p.stem: p for p in NOTES.rglob("*.md")}
    applied, missing = [], []

    for name, dates in uses.items():
        p = index.get(name)
        if not p:
            missing.append(name); continue
        text = p.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n?", text, flags=re.S)
        if not m:
            missing.append(f"{name} (no frontmatter)"); continue
        fm, body = m.group(1), text[m.end():]
        last, count = max(dates), len(dates)

        for key, val in (("last_used", last), ("used_count", count)):
            if re.search(rf"^{key}:", fm, flags=re.M):
                fm = re.sub(rf"^{key}:.*$", f"{key}: {val}", fm, count=1, flags=re.M)
            else:
                fm = fm.rstrip() + f"\n{key}: {val}"

        if not DRY:
            p.write_text("---\n" + fm + "\n---\n" + body, encoding="utf-8")
        applied.append((name, last, count))

    verb = "would update" if DRY else "updated"
    print(f"  {verb} {len(applied)} note(s)")
    for n, d, c in sorted(applied, key=lambda x: -x[2]):
        print(f"    {n[:56]:58} last_used {d}, used {c}×")
    if missing:
        print(f"\n  ⚠️  {len(missing)} log entr(ies) reference notes that do not exist:")
        for n in missing:
            print(f"    {n}")
        print("    Check the spelling, or the note may have been renamed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
