# Routines

Every routine starts the same way:

1. **Find the vault** (the path is usually given in the task prompt).
2. **Read `Admin/AGENTS.md`** in full. It is the authority; it wins over anything here.
3. **Read `Admin/wiki-settings.md`** for the user's email, newsletters, topics and time zone.

Then follow the routine's prompt file in the vault's `Admin/prompts/` folder — **the text below its `---` line** — treating every placeholder marked `←` (vault path, email, newsletter senders, topics, focus) as the matching value from `wiki-settings.md` or `AGENTS.md` §0. Never stop to ask for a placeholder that the settings file answers.

| Routine | Prompt file | Needs |
| --- | --- | --- |
| daily ingest | `Admin/prompts/daily-ingest.md` | — |
| your three | `Admin/prompts/your-three.md` | Gmail (for the heads-up email; carry on without it) |
| weekly lint | `Admin/prompts/weekly-lint.md` | — |
| newsletter sync | `Admin/prompts/newsletter-sync.md` | Gmail or Outlook connector; `newsletters` in settings |
| daily briefing | `Admin/prompts/daily-briefing.md` | web search; `briefing_topics` in settings |
| daily inspiration | `Admin/prompts/daily-inspiration.md` | `email` in settings → deliver by email via Gmail; otherwise make it your final reply |
| weak signals | `Admin/prompts/weekly-weak-signals.md` | only if `60 Signals/` exists |

If a needed connector or setting is missing, do as much as you can, and say in one line at the top of your reply what's missing and how to fix it (e.g. "Connect Gmail in Claude's connector settings so this can email you").

If the vault can't be reached, say in one line that the computer must be on with the Claude app open, and stop.

---

## Brief me (on demand)

"Brief me on X", "what do my notes say about X", "talking points on X". Follow `Admin/prompts/topic-briefing.md`. Read only — never edit notes during a briefing.

## Disagree or comment (on demand)

The user says they disagree with, or want to comment on, a note — e.g. "I don't buy the hydrogen note — costs aren't falling".

1. Find the note. If more than one could match, ask which, listing up to three by name.
2. Follow `Admin/AGENTS.md` §5a ("Owner review"):
   - A disagreement → a `> [!disagree] <owner>, <date>` box at the end of `## Why this matters`, in the user's own words, then your `> [!reply] Agent, <date>` box underneath: adjust `confidence` or correct the claim if warranted, or explain why the evidence still holds.
   - A comment that isn't a disagreement → a `> [!comment] <owner>, <date>` box.
   - If they also gave 1–5 scores, write `importance`, `fit`, `reviewed`, `reviewed_corroborations`.
3. Append one line to `00 Inbox/_review-log.md`.
4. Confirm in one or two lines what you wrote and changed.

## Remove the example notes (on demand)

Agents never delete notes, so **list** the files tagged `example` (in `10 Notes/`, `Clippings/`, `40 Archive/Processed captures/`, and `60 Signals/` if present) and the example line in `Admin/Attention log.md`, and ask the user to delete them in Obsidian. If the user explicitly asks you to delete them and your file access allows it, delete exactly those files and nothing else.
