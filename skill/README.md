# The obsidian-wiki skill (beta)

A guided way to install everything in this kit. Instead of following [SETUP.md](../SETUP.md), you upload one file to Claude, connect an empty folder, and say **"set up my wiki"**. Claude interviews you, builds the vault, sets up the scheduled tasks and runs a first ingest with you. No terminal.

> **Beta.** It's being tested now. The manual guide in [SETUP.md](../SETUP.md) remains the proven route, especially on Windows.

## Install

1. **Download** [`dist/obsidian-wiki.zip`](../dist/obsidian-wiki.zip). Don't unzip it.
2. In Claude, check **Settings → Capabilities → Code execution and file creation** is on (also called **Create and edit files**).
3. Go to **Customize → Skills → + → Create skill → Upload a skill**, and choose the zip.
4. Install **[Obsidian](https://obsidian.md)**, but don't open a vault yet.
5. Create an **empty folder** for your wiki, outside iCloud Drive, OneDrive and Dropbox, e.g. `~/Obsidian/My Wiki` or `C:\Vaults\My Wiki`.
6. In the Claude desktop app, start a task with that folder connected and say: **"Set up my wiki in this folder."**

About 15 minutes, start to finish.

## What it does

1. Checks the folder location and Gmail connection
2. Asks five questions: your name, focus, extra category, optional features and time zone
3. Builds the vault, with Dataview and Git pre-installed for Obsidian
4. Walks you through opening it in Obsidian
5. Sets up the scheduled tasks (you confirm each one)
6. Ingests an article you choose, so you see it work
7. Walks you through turning on backups
8. Summarises what happens next

Afterwards, the scheduled tasks call the skill, so their prompts are one line each. To update: upload the new zip, then say **"update my wiki"**.

## What it can't do

- **Install software on your computer.** Backups need git installed (one standard installer); Claude walks you through it.
- **Back up while Obsidian is closed.** The Git plugin saves a snapshot every hour while Obsidian is open.
- **Run tasks while your computer is off.** The computer must be on with the Claude app open at task times.

## Building it

`python3 tools/build_skill.py` assembles `skill/obsidian-wiki/` with `vault/` and `addons/weak-signals/` as assets, and writes `dist/obsidian-wiki.zip`. Edit the vault and add-on in their own folders, never inside the skill, so there's one source for every file. The bundled Obsidian plugins (Dataview and Git) are MIT-licensed; their licences are included.
