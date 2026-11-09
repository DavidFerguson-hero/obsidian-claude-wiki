# Scheduled task prompts

The prompts behind the automations. Scheduled tasks belong to your own Claude account, so they can't be installed for you — but you don't have to copy them by hand either.

**Easiest:** paste [`00 Set up my scheduled tasks`](00%20Set%20up%20my%20scheduled%20tasks.md) into a Claude conversation with your vault folder connected. Claude asks a few questions, fills in each prompt, and sets the tasks up.

**By hand:** in the Claude desktop app, go to **Scheduled → New task → Set up manually**, paste the text below the `---` line of a prompt, fill in every `←` placeholder, choose your vault folder, and set the schedule below.

| Prompt | Suggested time | Writes to | Needed? |
| --- | --- | --- | --- |
| [`daily-ingest.md`](daily-ingest.md) | Daily 05:50 | `10 Notes/`, `40 Archive/` | **Core** — the engine |
| [`your-three.md`](your-three.md) | Sundays 09:20 | `10 Notes/` (your ratings only) | **Core** — where your judgement goes in. Emails you when it's waiting (Gmail connector) |
| [`weekly-lint.md`](weekly-lint.md) | Sundays 08:10 | `Admin/_LINT.md` only | **Core** — the weekly health check |
| [`newsletter-sync.md`](newsletter-sync.md) | Daily 05:10 | `00 Inbox/` | Optional — copies your email newsletters in (Gmail or Outlook connector) |
| [`daily-briefing.md`](daily-briefing.md) | Weekdays 05:25 | `00 Inbox/` | Optional — a daily news round-up on your topics |
| [`daily-inspiration.md`](daily-inspiration.md) | Daily 07:40 | `00 Inbox/_inspiration-log.md` only | Optional — one random note emailed to you each day, with news and ideas (Gmail connector) |
| `weekly-weak-signals.md` | Sundays 08:35 | `60 Signals/` | Add-on only — copied here when you install it |
| [`topic-briefing.md`](topic-briefing.md) | Not scheduled | nothing | Use in chat any time: "brief me on X" |

**Why this order.** Inputs (newsletters, briefing) land before the ingest reads them; the ingest finishes before the weekly runs; everything finishes before the nightly backup at 21:00, so each day's changes land in one commit you can review.

**Your computer must be on, with the Claude app open, at these times.** The tasks work on files on your computer. If it's off, that run is missed.

**One writer at a time.** The daily ingest is a second writer alongside any chat where you ask Claude to edit notes. If notes start appearing with the wrong frontmatter, the scheduled prompt has drifted from `Admin/AGENTS.md` — fix the prompt, don't hand-repair dozens of notes.
