# Scheduled task prompts

These are the prompts behind the automations. Scheduled tasks belong to your own Claude account, so they can't be bundled — copy each prompt into a new scheduled task instead.

**How:** in the Claude desktop app, open your vault's Project → create a scheduled task → paste the prompt → pick the schedule below. Make sure the task can reach your vault folder.

| Prompt | Suggested schedule | Writes to | Needed? |
| --- | --- | --- | --- |
| [`daily-ingest.md`](daily-ingest.md) | Daily, early morning | `10 Notes/`, `40 Archive/` | **Core** — this is the engine |
| [`your-three.md`](your-three.md) | Weekly, e.g. Sunday morning | `10 Notes/` (your ratings) | **Core** — where your judgement goes in |
| [`weekly-lint.md`](weekly-lint.md) | Weekly, e.g. Sunday | `Admin/_LINT.md` only | Recommended |
| [`daily-briefing.md`](daily-briefing.md) | Weekdays, before ingest | `00 Inbox/` | Optional — feeds the inbox from the web |
| [`newsletter-sync.md`](newsletter-sync.md) | Daily, an hour before ingest | `00 Inbox/` | Optional — copies your email newsletters in (needs Gmail or Outlook connector) |
| [`daily-inspiration.md`](daily-inspiration.md) | Daily, when you'll read it | nothing (reads only) | Optional — one random note back to you each day, with news and ideas |
| [`topic-briefing.md`](topic-briefing.md) | Not scheduled — use on demand | nothing | Optional |
| Weak signals | Weekly | `60 Signals/` | Add-on — see [`addons/weak-signals`](../addons/weak-signals) |

**Order matters.** If you run the briefing, schedule it *before* the ingest so the ingest picks it up the same day. Schedule your nightly backup (`backup_vault.py --install`) *after* all of them, so each day's agent changes land in one commit you can review.

**One writer at a time.** The daily ingest is a second writer alongside any chat where you ask Claude to edit notes. If notes start appearing with the wrong frontmatter, the scheduled prompt has drifted from `Admin/AGENTS.md` — fix the prompt, don't hand-repair dozens of notes.
