# Claude Project instructions

Paste everything below the line into the instructions of the Claude Project you use with this vault. Keep it short on purpose: the real rules live in `AGENTS.md`, and a second copy would drift.

---

## This Project works on my Obsidian vault

**Before creating or editing anything in `10 Notes/`, read `Admin/AGENTS.md`.** It is the only authority for note structure, frontmatter and operations. If anything here disagrees with it, AGENTS.md wins — flag the conflict.

The vault is a compiled wiki, not a filing cabinet. I feed it (clippings, newsletters, my own notes); you keep it in shape.

### Folders

```
00 Inbox/      — Unprocessed captures. Ingest reads them, then archives them.
05 Sources/    — Immutable source material. Never edit.
10 Notes/      — The compiled wiki. Yours to read and write. Filed by category.
20 Personal/   — Mine. Read only.
30 Resources/  — Reference material and attachments.
40 Archive/    — Append only.
60 Signals/    — Weak-signals register (only if the add-on is installed).
Clippings/     — Raw web captures. Read only.
Admin/         — AGENTS.md, templates, attention log, lint report. Read only.
*.py           — Scripts, in the vault root.
```

### Rules worth repeating because they are easy to get wrong

1. Count `corroborations` and `independent_sources` **only** inside `## Supporting evidence`.
2. Never invent a date, a source or a count. `unknown` is fine.
3. Never delete a note. Propose it.
4. Never rewrite my own prose. Move it under `## Thoughts (original)` and build around it.
5. Never overwrite a `strength_basis: assessed` value.
6. Never set `last_used` / `used_count` — only `apply_attention.py` does.
7. Never run `git clean`.
8. If a task needs writing outside `10 Notes/`, stop and ask.
9. Never set `importance` or `fit` — only my answers do. If I disagree with a note in chat, file it as a `> [!disagree]` box in my words and reply underneath (AGENTS.md §5a). Never edit or remove a `[!disagree]` box.

### Scripts

| Script | Does |
| --- | --- |
| `lint_wiki.py` | Writes `Admin/_LINT.md`. Reports only, never edits. |
| `apply_attention.py` | Copies `Admin/Attention log.md` entries into note frontmatter. |
| `build_signals_json.py` | (Add-on) Builds `signals.json` from `60 Signals/`. |

### Where new work goes

New research and insights go to `00 Inbox/`. They only enter `10 Notes/` through the ingest operation (AGENTS.md §7), which prefers updating existing notes over creating new ones.
