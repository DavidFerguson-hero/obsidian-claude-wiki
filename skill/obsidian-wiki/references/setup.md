# Guided setup

Goal: take the user from an empty folder to a working, scheduled wiki in one conversation, with no terminal. Keep every message short, plain English, one step at a time. Tell the user roughly how long each part takes. Number the stages so they can see progress:

1. Check the basics · 2. Five questions · 3. Build the vault · 4. Open it in Obsidian · 5. Scheduled tasks · 6. First real ingest · 7. Backups · 8. Done

Use tappable multiple-choice questions where your app supports them; otherwise ask in plain text.

---

## 1. Check the basics (1 min)

1. **Find the folder.** The connected folder should be empty (hidden files like `.DS_Store` are fine). If it already contains `Admin/AGENTS.md`, this is an existing wiki — offer `references/update.md` instead, and stop. If it contains other files, ask whether to use it anyway (nothing will be overwritten) or to pick an empty folder.
2. **Check the location.** If the folder path contains `iCloud`, `Mobile Documents`, `OneDrive`, `Dropbox` or `Google Drive`, warn the user: sync services and backups conflict, and cloud-only files can be invisible to Claude. Recommend `~/Obsidian/My Wiki` (Mac) or `C:\Vaults\My Wiki` (Windows). Continue only if they insist.
3. **Check Gmail.** If a Gmail connector is available in this conversation, note it. If not, tell the user in one line that the weekly review and daily inspiration send emails, and they can connect Gmail in Claude's connector settings now or later. Don't block on it.
4. **Check Obsidian.** Ask whether Obsidian is installed. If not: "Download it free from obsidian.md — install it, but don't open a vault yet. Tell me when it's done." You can carry on with stage 2 while they do.

## 2. Five questions (3 min)

Ask in **one message**, numbered. Give the example answers so they know the level of detail wanted.

1. **Your name.**
2. **Your focus** — what should every note be judged against? *e.g. "my role leading innovation at a UK energy company", "my climate-tech VC fund", "my PhD on urban heat"*. Push back gently if it's vague ("sustainability"): a specific focus makes every "so what" better.
3. **Your extra category.** Notes are filed by PESTLE (Political, Economic, Social, Technological, Legal, Environmental) plus one category of your own. *e.g. Energy, Health, Finance, Education* — or none.
4. **Optional extras** — which would you like?
   - **Newsletter sync** — copies your email newsletters into the inbox (needs Gmail). If yes: which sender addresses?
   - **Daily briefing** — a weekday news round-up on topics you choose. If yes: which 3–5 topics?
   - **Daily inspiration** — one forgotten note emailed to you each morning with news and ideas (needs Gmail). If yes: which email address?
   - **Weak signals** — a big-picture register of signals and themes. Recommend **not yet** for a new vault: it needs 50+ notes.
5. **Your time zone**, and whether early-morning processing (05:00–06:00) suits — the computer must be on with the Claude app open then.

## 3. Build the vault (1 min)

1. Write the answers to a JSON file in your working area (not in the vault):

   ```json
   {
     "owner": "Ana Silva",
     "vault_path": "/Users/ana/Obsidian/My Wiki",
     "focus": "my role leading innovation at a UK water company",
     "so_what": "What does this mean for my innovation team?",
     "extra_category": "Water",
     "email": "ana@example.com",
     "newsletters": ["news@example.com"],
     "briefing_topics": ["water policy", "leak detection"],
     "timezone": "Europe/London",
     "features": {"newsletter_sync": true, "daily_briefing": false, "daily_inspiration": true, "weak_signals": false}
   }
   ```

   `vault_path` is the folder's path **as the user's own computer shows it** (e.g. `C:\\Vaults\\My Wiki` or `/Users/ana/Obsidian/My Wiki`) — not the path your shell uses, if that differs. Scheduled tasks use it. `so_what` is "What does this mean for …?" built from their focus. `extra_category` is a single word in title case, or `null` for none. Leave unknown values as `null` or `[]`.

2. Run the installer (see "Running the bundled scripts" in `SKILL.md`):

   ```
   python3 scripts/install_vault.py --target "<vault folder>" --answers "<answers.json>"
   ```

3. It prints a JSON summary. If `ok` is false, tell the user what went wrong in plain words and stop.
4. Run the vault's checker: from the vault folder, `python3 check_setup.py --agent`. Fix anything it reports that you can fix (it explains each item).

## 4. Open it in Obsidian (2 min)

Tell the user exactly this, as a numbered list:

1. Open Obsidian → **Open folder as vault** → choose *<folder name>*.
2. When asked whether to trust the author and enable plugins, click **Trust author and enable plugins**. (That turns on the two plugins already installed: **Dataview**, which draws the dashboards, and **Git**, which backs up.)
3. Open **+Home** in the left sidebar. You should see tables with three example notes.

Ask them to confirm. If they see blocks of code instead of tables: Settings → **Community plugins** → make sure **Restricted mode** is off and **Dataview** is enabled.

## 5. Scheduled tasks (3 min)

Create these scheduled tasks using the scheduling tool available in this conversation, each one **with the vault folder attached** so it runs on the user's computer. Show each proposed task (name, schedule, prompt) and let the user confirm.

Each task's prompt is **one line** — the routine itself lives in this skill and the vault:

> Use the obsidian-wiki skill to run the **<routine name>** routine on my vault at `<vault path>`.

| Task name | Routine name | Default time (user's time zone) | When |
| --- | --- | --- | --- |
| Newsletter sync | newsletter sync | 05:10 daily | if chosen |
| Daily briefing | daily briefing | 05:25 weekdays | if chosen |
| Daily ingest | daily ingest | 05:50 daily | always |
| Daily inspiration | daily inspiration | 07:40 daily | if chosen |
| Weekly lint | weekly lint | 08:10 Sundays | always |
| Your three | your three | 09:20 Sundays | always |

Use the user's preferred times if they gave them, keeping this order. Turn on push notifications for **Your three** if the tool allows.

**If you can't create scheduled tasks from this conversation**, give the user each task ready to paste — name, schedule and the one-line prompt — with these instructions: in the Claude app, **Scheduled → New task → Set up manually**, paste the prompt, choose the vault folder, set the time, **Save**.

## 6. First real ingest (3 min)

Much more convincing than an example. Ask: "Paste a link to an article you'd want in your wiki — anything you've read recently."

1. Save it as a capture in `00 Inbox/` (title, `source_url`, date, and the article's main text if you can fetch it; otherwise the link and a two-line description of what it says).
2. Run the **daily ingest** routine on it now (`references/routines.md`).
3. Show the result in 3–4 bullets: which notes changed or were created, and one line on why. Point them to the note in Obsidian.

## 7. Backups (2 min, recommended)

The **Git** plugin is installed and set to save a snapshot every hour while Obsidian is open. It needs **git** on the computer and the vault set up as a repository. Guide the user:

1. **Install git if needed.**
   - Mac: Applications → Utilities → **Terminal**, type `git --version`, press Return. If a box offers to install **Command Line Tools**, click **Install** (about 5 minutes). If it shows a version number, git is already there.
   - Windows: download from **git-scm.com/download/win**, run it, click **Next** through every screen.
2. **Turn the vault into a repository.** In Obsidian, press **Ctrl/Cmd + P**, type `Git: Initialize a new repo`, press Enter. Then **Ctrl/Cmd + P** → `Git: Commit all changes`.
3. **Check:** the bottom-right status bar shows the Git plugin with no error.

Optional off-computer copy: a **private** GitHub repository. Point them to the plugin's own guide for connecting a remote, and tell them to switch **Disable push** off in the Git plugin's settings afterwards.

Don't run `git` commands yourself in the vault: Claude's file access can leave lock files that jam git.

## 8. Done (1 min)

Finish with a short summary:

- **Your wiki:** the folder path, and "start at +Home".
- **Feed it:** clip articles with the Obsidian Web Clipper into `Clippings/` (obsidian.md/clipper), forward or drop newsletters and notes into `00 Inbox/`.
- **Each Sunday:** "Your three" sends three questions — reply in one line. Explain the two 1–5 scores in one line each.
- **Any time:** "brief me on X", or "I disagree with the note on X because…".
- **The table of scheduled tasks** you set up, and: "Your computer needs to be on, with the Claude app open, at these times."
- **One line for the Project:** if they use a Claude Project for this wiki, suggest pasting this into its instructions so chats always use the skill:

  > This Project works on my Obsidian wiki at `<vault path>`. For anything involving it, use the obsidian-wiki skill and read `Admin/AGENTS.md` first.

- **After a week or two:** ask Claude to "remove the example notes from my wiki".
