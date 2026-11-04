# Weekly lint

Copy everything below the line into a scheduled task.

---

Run a health check on my Obsidian vault at `PATH/TO/YOUR/VAULT` ← replace this.

1. Read `Admin/AGENTS.md` §7 (Lint) so you know what the checks mean.
2. Run `python3 apply_attention.py`, then `python3 lint_wiki.py`, from the vault root. These write `Admin/_LINT.md` and touch only `last_used` / `used_count` fields.
3. **Do not fix anything.** Lint reports; it never edits, and neither do you in this task.
4. Send me a short summary (no more than 8 bullets):
   - The three most useful things to look at this week, with the note names.
   - Any newly written note showing up under "Section drift" or "Schema drift" — that means the daily ingest has drifted from AGENTS.md.
   - The top item under "Overdue assessment", phrased as a question I can answer in one line.
