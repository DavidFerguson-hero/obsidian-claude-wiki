---
name: obsidian-wiki
description: Sets up and runs an Obsidian vault Claude maintains as a wiki. Use for wiki setup or update, ingest, Your three, brief me, disagreeing with a note, lint, newsletter sync, inspiration.
---

# Obsidian wiki

This skill sets up and runs an **Obsidian vault that Claude maintains as a compiled wiki**: the user feeds it captures, Claude folds the evidence into existing notes, and the user rates and disagrees once a week.

## The one rule that matters most

**The vault's own `Admin/AGENTS.md` is the only authority for how notes are written.** This skill installs and updates it, but never keeps a second live copy of the rules. For any routine below, read the vault's `Admin/AGENTS.md` first and follow it. If this skill and `AGENTS.md` ever disagree, `AGENTS.md` wins.

## Find the vault

The vault is the connected folder that contains `Admin/AGENTS.md`. If none does and the user wants setup, use an **empty** connected folder. If no folder is connected, ask the user to connect one (and, if they're starting fresh, to create an empty folder first, outside iCloud Drive, OneDrive and Dropbox).

The user's choices (email, newsletters, topics, time zone) live in `Admin/wiki-settings.md`. Read it at the start of every routine.

## What do you need to do?

| The user wants… | Do this |
| --- | --- |
| To set up a new wiki ("set up my wiki", "install") | Follow `references/setup.md` |
| To update to a newer version of this skill | Follow `references/update.md` |
| A **scheduled routine** (daily ingest, Your three, weekly lint, newsletter sync, daily briefing, daily inspiration, weak signals) | Follow `references/routines.md` |
| A briefing ("brief me on X", "what do my notes say about X") | `references/routines.md` → Brief me |
| To disagree or comment ("I don't buy the hydrogen note") | `references/routines.md` → Disagree |
| Anything else in the vault | Read `Admin/AGENTS.md` and follow it |

## Running the bundled scripts

`scripts/install_vault.py` builds and updates vaults from `assets/`. It needs Python 3.8+ and must run in a shell that can see **both** this skill's folder and the vault folder.

If they're not visible from one shell — for example, the skill runs in Claude's environment but the vault is on the user's computer through a separate file bridge — then copy `scripts/` and `assets/` into the vault folder as one zip named `_wiki-setup.zip`, unzip it inside the vault into `_wiki-setup/`, and run the installer from there. Tell the user they can delete `_wiki-setup/` and the zip afterwards (the installer doesn't delete files).

The vault's own scripts (`lint_wiki.py`, `random_note.py`, `check_setup.py`, …) are installed into the vault root and always run from there, e.g. `python3 lint_wiki.py`. If `python3` isn't found, try `python`, then `py`.

## Ground rules for every routine

- Never delete a note. Never run `git clean`. Never invent a date, source or count.
- Never set or change `importance` / `fit`, and never touch a `[!disagree]` or `[!comment]` box — only the user's own answers set those.
- Keep messages to the user short and in plain English.
