# Daily ingest

Copy everything below the line into a scheduled task.

---

You are maintaining my Obsidian vault, a compiled wiki. The vault folder is: `PATH/TO/YOUR/VAULT` ← replace this.

**Step 0 — read the rules.** Read `Admin/AGENTS.md` in full before doing anything else. It is the only authority on note structure, frontmatter and operations. Do not rely on any memory of it from earlier runs; it may have changed. If §0 still contains `TODO`, stop and report that I need to fill it in.

**Step 1 — find new captures.** List files in `00 Inbox/` and `Clippings/` that do not have `inbox_processed: true` in their frontmatter. Ignore files whose names start with `_`. Ignore empty stubs. If there is nothing new, write one line to `00 Inbox/_processing-log.md` saying so and stop.

**Step 2 — ingest each capture** using the Ingest operation in AGENTS.md §7:
- Expect each capture to touch 5–15 existing notes. Search `10 Notes/` properly before deciding a topic has no home.
- Prefer updating existing notes. Create a new note only if the topic genuinely has no home, using `Admin/_templates/Compiled Note.md`.
- Add evidence in the house style with the `*(YYYY-MM-DD)*` date of the evidence itself, not today's date, unless the capture gives no date.
- Recount `corroborations` and `independent_sources` from `## Supporting evidence` only.
- Never overwrite a `strength_basis: assessed` value. If new evidence bears on an assessment, follow §7 step 3 exactly.
- If a concept note is touched, apply the lazy reformat rule (§3) — my prose moves under `## Thoughts (original)` unchanged.

**Step 3 — archive.** For every capture you finished, follow "Archive on completion" in §7: flag it, move it to `40 Archive/Processed captures/`, rewrite any `sources:` paths that pointed at the old location, and log the move.

**Step 4 — report.** Append a short entry to `00 Inbox/_processing-log.md`: each capture processed, each note changed with a one-line reason, and anything you were unsure about.

**Never:** delete a note, edit `05 Sources/`, `20 Personal/` or `60 Signals/`, invent a date, source or count, set `last_used` / `used_count`, run `git` commands, or run `git clean`.
