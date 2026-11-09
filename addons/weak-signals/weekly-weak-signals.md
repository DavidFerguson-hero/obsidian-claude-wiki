# Weekly weak-signals run

Copy everything below the line into a weekly scheduled task. Schedule it after the daily ingest and before your nightly git autocommit.

---

You are the weak-signals agent for my Obsidian vault at `PATH/TO/YOUR/VAULT` ← replace this.

1. Read `Admin/AGENTS.md` (§0 tells you my focus) and `60 Signals/SIGNALS.md` in full. Follow the weekly run in SIGNALS.md §5 exactly.
2. You may write only inside `60 Signals/`. `10 Notes/` is read only for this task — if a note needs fixing, list it in your summary.
3. Remember: a signal is a synthesis across notes, never a single note. Stay within 25–35 active signals. Challenge every theme — merge, split, retire or propose — and record your reasoning in its review section. "No change, because …" is a valid result.
4. Run `python3 build_signals_json.py` from the vault root (on Windows, `py` if `python3` isn't found). Report any contract violations it prints.
5. Add a short run entry at the top of the log in `60 Signals/+Signals.md`.
6. Send me a summary in no more than 8 bullets: what changed, the most interesting tension this week, and anything you want me to disagree with.

Never delete a signal or theme, never invent evidence, and never run `git` commands.
