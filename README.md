# Obsidian + Claude: a self-maintaining knowledge wiki

A starter kit for running an Obsidian vault that Claude maintains for you. **You feed it; Claude keeps it in shape.**

You drop articles, newsletters and your own thinking into an inbox. Every morning Claude reads them and folds the evidence into the notes you already have — dated, cited, counted — rather than adding yet another note. Weekly, a health check tells you which ideas are gaining evidence, which have gone quiet, and where your notes contradict each other. Your own writing is never rewritten.

It's based on Andrej Karpathy's "LLM wiki" idea, hardened over several months of daily use by [David Ferguson](https://github.com/DavidFerguson-hero).

## What's in the box

| | What | Where |
| --- | --- | --- |
| 📁 | **Starter vault** — folders, templates, index pages, example notes | [`vault/`](vault) |
| 📜 | **`AGENTS.md`** — the rulebook Claude follows. The heart of the system | [`vault/Admin/AGENTS.md`](vault/Admin/AGENTS.md) |
| 🧪 | **Scripts** — a setup checker, a health check (lint), usage tracking, nightly git backup — all plain Python, same on Mac and Windows | [`vault/`](vault) |
| ⏰ | **Scheduled task prompts** — daily ingest, weekly "Your three" review, weekly lint, optional news briefing | [`prompts/`](prompts) |
| 📡 | **Weak-signals add-on** — big-picture register of 25–35 signals and themes | [`addons/weak-signals/`](addons/weak-signals) |
| 📖 | **How it works** — the design, and the lessons learned the hard way | [`docs/how-it-works.md`](docs/how-it-works.md) |

## How it works in one picture

```
   YOU                          CLAUDE (scheduled)                        YOU
   ───                          ──────────────────                        ───
 clippings ─┐                 ┌─► daily ingest ──► 10 Notes/ ──┐
 newsletters├─► 00 Inbox/ ────┤   (updates 5–15 existing notes,│
 own notes ─┘                 │    counts sources, archives)   ├─► +Home, dashboards,
                              │                                │   briefings on demand
                              ├─► weekly lint ───► _LINT.md ───┘
                              │
                              └─► "Your three" ──► 3 questions ──► you reply in one line:
                                  (weekly)         on your phone    does it matter? does it fit?
                                                   │
                     add-on:  weekly signals ──► 60 Signals/ ──► signals.json
```

**Who does what.** Claude owns the *evidence*: counting, dating and linking sources. You own the two things only you can judge — **does it matter?** and **does it match what you see?** — answered once a week in one line. When you disagree, your words go into the note in a box agents can never edit, and the agent has to reply.

## Quick start

Works on **Mac and Windows** (and Linux). You need [Obsidian](https://obsidian.md), the Claude desktop app on a paid plan with scheduled tasks, Python 3.8+ and git.

1. Click **Use this template** (or download the zip) and copy the `vault/` folder to where you want your vault.
2. Open it in Obsidian and install the **Dataview** community plugin.
3. Fill in **§0 of `Admin/AGENTS.md`** — your name and the focus every note is judged against.
4. Create a Claude Project, connect the vault folder, and paste in `Admin/PROJECT-INSTRUCTIONS.md`.
5. Set up the daily ingest scheduled task from [`prompts/daily-ingest.md`](prompts/daily-ingest.md).

**Full walkthrough, about 30 minutes: [SETUP.md](SETUP.md).**

## Who it's for

People who read a lot for work and want that reading to compound — strategy, research, policy, investment, innovation roles. It suits you if you're comfortable with Terminal for a few commands. You don't need to write code.

It's opinionated. It assumes a few dozen captures a week, judged against one focus (an organisation, a role or a research question). It won't suit a personal journal or a task manager.

## Problems and ideas

Please [open an issue](../../issues). Say what you expected, what happened, and paste the relevant part of `Admin/_LINT.md` or the processing log if you have it.

## Licence

- Code (`*.py`, `*.sh`): [MIT](LICENSE)
- Docs, prompts, templates and `AGENTS.md`: [CC BY 4.0](LICENSE-docs.md) — reuse and adapt freely, with credit.
