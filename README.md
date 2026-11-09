# Obsidian + Claude: a knowledge wiki that maintains itself

**You feed it. Claude keeps it in shape. You stay the judge.**

A ready-to-use [Obsidian](https://obsidian.md) vault, plus the rules and scheduled tasks that let Claude maintain it for you. Works on **Mac and Windows**.

You drop articles, newsletters and your own thinking into an inbox. Every morning Claude reads them and folds the evidence into the notes you already have — dated, cited and counted — instead of piling up yet another note. Once a week it asks you three quick questions, so the vault knows what *you* think matters. Your own writing is never rewritten.

Based on Andrej Karpathy's "LLM wiki" idea, and hardened over months of daily use by [David Ferguson](https://github.com/DavidFerguson-hero).

**→ [Install and set up](SETUP.md)** — about 45 minutes, with every step spelled out.

---

## What it does for you

| Every day | Every week | Whenever you want |
| --- | --- | --- |
| New clippings and newsletters are folded into your existing notes, with sources counted and dated | **"Your three":** Claude asks you to rate three notes. You reply in one line from your phone | "Brief me on *X*": an answer drawn from your own notes, with sources |
| *Optional:* your newsletters copied in from email | A health check flags what's gaining evidence, what's gone quiet and where notes contradict each other | Disagree with any note. Your words are kept in a box agents can't edit, and the agent has to reply |
| *Optional:* one forgotten note emailed back to you, with related news and five ideas | *Add-on:* a big-picture register of 25–35 signals and themes | Every change is backed up nightly, so you can see it and undo it |

## How it works

```
  YOU FEED IT                 CLAUDE MAINTAINS IT                    YOU JUDGE IT
  ───────────                 ───────────────────                    ────────────
  web clippings ─┐
  newsletters  ──┼─► 00 Inbox ──► daily ingest ──► 10 Notes ──┐
  your own notes ┘               (updates 5–15                │
                                  existing notes,             ├──► +Home dashboards
                                  counts sources)             │
                                                              ├──► weekly "Your three"
                                 weekly health check ◄────────┘     importance 1–5
                                                                    fit 1–5
                                                                    one-line reply
```

**Who does what.** Claude owns the **evidence**: finding, counting, dating and linking sources. You own the two things only you can judge — **does it matter?** and **does it match what you see?** It's built so you never have to tidy, tag or file anything. If the system needs you to maintain it, it has failed.

## What you need

- A **Mac or Windows** computer, **on with the Claude app open** when the tasks run (early morning, by default)
- A **paid Claude plan** and the **[Claude desktop app](https://claude.ai/download)**
- **[Obsidian](https://obsidian.md)** (free)
- **Python** and **git**, both free. The setup guide walks you through installing them
- *Recommended:* **Gmail** connected to Claude, for the weekly review and daily inspiration emails

You'll paste about ten commands into a terminal during setup. You don't need to write code.

## What's in the box

| | | |
| --- | --- | --- |
| 📁 **[`vault/`](vault)** | **The vault itself.** Move this folder to your computer and open it in Obsidian | Folders, templates, dashboards and three example notes |
| 📜 [`vault/Admin/AGENTS.md`](vault/Admin/AGENTS.md) | **The rulebook Claude follows.** The heart of the system. You fill in one section | |
| ⏰ [`vault/Admin/prompts/`](vault/Admin/prompts) | **The scheduled tasks.** One prompt sets them all up for you | Daily ingest, Your three, weekly lint; optional newsletter sync, daily briefing and daily inspiration |
| 🧪 Scripts in `vault/` | **Small helpers**, plain Python, the same on Mac and Windows | `check_setup.py` · `backup_vault.py` · `lint_wiki.py` · `random_note.py` · `apply_attention.py` |
| 📡 [`addons/weak-signals/`](addons/weak-signals) | **Optional add-on** for when you have 50+ notes | Big-picture signals, themes and an interactive map |
| 📖 [`docs/how-it-works.md`](docs/how-it-works.md) | **The design**, and 13 lessons learned the hard way | |

## Setup at a glance

Full instructions: **[SETUP.md](SETUP.md)**.

1. **Install the tools:** Python, git, Obsidian and the Claude desktop app.
2. **Get the vault:** download this repository, and move the `vault` folder somewhere that isn't iCloud, OneDrive or Dropbox.
3. **Open it in Obsidian** and install the Dataview plugin.
4. **Tell it your focus:** fill in section 0 of `Admin/AGENTS.md`.
5. **Connect Claude:** create a Project, paste in the instructions, and connect the folder.
6. **Turn on backups:** `python3 backup_vault.py --install`.
7. **Check it:** `python3 check_setup.py`.
8. **Automate it:** paste one prompt and Claude sets up the scheduled tasks.

## Who it's for

People who read a lot for work and want that reading to compound: strategy, research, policy, investment and innovation roles. It works best with a few dozen captures a week, judged against one clear focus such as an organisation, a role or a research question.

It's not a journal, a task manager or a place for meeting notes.

## Problems and ideas

[Open an issue](../../issues/new/choose). The template asks for the output of `python3 check_setup.py`, which answers most questions. Ideas, and stories of agents going wrong in ways the rules didn't prevent, are especially welcome.

## Licence

- **Code** (`*.py`): [MIT](LICENSE)
- **Docs, prompts, templates and `AGENTS.md`:** [CC BY 4.0](LICENSE-docs.md). Reuse and adapt freely, with credit.
