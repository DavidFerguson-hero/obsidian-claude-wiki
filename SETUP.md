# Install and set up

This guide takes you from nothing to a vault that Claude maintains for you every day. It works on **Mac** and **Windows**.

- **Time:** about 45 minutes, in one sitting.
- **Skill level:** you'll paste about ten commands into a terminal. You don't need to write code or understand the commands.
- **How each step works:** what you'll do, **do this**, ✅ **you should see**, and what to do if you don't.

> If anything goes wrong at any point, run the setup checker (step 9). It tells you in plain words what's missing.

---

## Before you start

### Check you have these

| You need | Why | Cost |
| --- | --- | --- |
| A **Mac** or **Windows** PC | Where your vault lives | — |
| A **paid Claude plan** (Pro, Max, Ultra, Team or Enterprise) | Scheduled tasks need a paid plan | Paid |
| The **[Claude desktop app](https://claude.ai/download)** | Runs the scheduled tasks on your files | Free download |
| **[Obsidian](https://obsidian.md)** | Where you read and write notes | Free |
| A **Gmail** account connected to Claude *(recommended)* | The weekly review and daily inspiration email you | Free |
| A **GitHub** account *(optional)* | Off-computer backup of your vault | Free |

On a Team or Enterprise plan, your admin may need to switch on Cowork or scheduled tasks for you.

### Three things to know before you start

1. **Your computer must be on, with the Claude app open, when tasks run.** The tasks work on files on your computer. If it's off at 05:50, that morning's update waits until the next day.
2. **Keep the vault out of iCloud Drive, OneDrive and Dropbox.** Sync services fight with the backup, and files stored only in the cloud can be invisible to Claude. **Windows often puts Documents and Desktop inside OneDrive without telling you**, so on Windows use `C:\Vaults\`.
3. **You only edit one file.** Step 5 is the only time you edit the rulebook. Everything else is clicking and pasting.

---

## Part 1 — Install the tools (10 min)

### Step 1. Open a terminal

You'll use this a few times. A terminal is a window where you type commands.

<details>
<summary><b>Mac</b></summary>

Press **⌘ Space**, type `Terminal`, press **Return**.

</details>

<details>
<summary><b>Windows</b></summary>

Press the **Windows key**, type `Terminal` (Windows 11) or `PowerShell` (Windows 10), press **Enter**.

</details>

✅ **You should see** a window with a blinking cursor.

### Step 2. Install Python and git

**Python** runs the vault's small helper scripts. **git** keeps a history of every change, so you can always undo.

<details>
<summary><b>Mac</b></summary>

Paste this into the terminal and press **Return**:

```
python3 --version; git --version
```

- ✅ If you see two version numbers (e.g. `Python 3.12.4`, `git version 2.39`), you're done.
- If a box pops up offering to install **Command Line Tools**, click **Install**, wait about 5 minutes, then run the command again.

</details>

<details>
<summary><b>Windows</b></summary>

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download Python.
2. Run the installer. On the first screen, **tick "Add python.exe to PATH"**, then click **Install Now**.
3. Go to [git-scm.com/download/win](https://git-scm.com/download/win), download git, and run the installer. Click **Next** through every screen, keeping the defaults.
4. **Close the terminal and open a new one** (step 1). Then paste:

   ```
   py --version; git --version
   ```

- ✅ **You should see** two version numbers.
- If `py` isn't recognised, re-run the Python installer, choose **Modify**, and make sure **py launcher** and **Add to PATH** are ticked.
- If typing `python` opens the Microsoft Store, ignore it and use `py`, as this guide does.

</details>

> **From here on:** where this guide says `python3`, Windows users type `py`.

### Step 3. Install Obsidian and the Claude app

1. Install **[Obsidian](https://obsidian.md)**.
2. Install the **[Claude desktop app](https://claude.ai/download)** and sign in.
3. *Recommended:* in the Claude app, open **Settings → Connectors** and connect **Gmail**.

---

## Part 2 — Get the vault (10 min)

### Step 4. Download the kit and put the vault in place

1. On this repository's GitHub page, click the green **Code** button → **Download ZIP**.
2. Unzip it (double-click on Mac; right-click → **Extract All** on Windows). You get a folder called `obsidian-claude-wiki-main`.
3. Inside it, find the folder called **`vault`**. That folder *is* your vault; everything else is documentation and extras.
4. Move `vault` to its permanent home and rename it, for example to `My Wiki`:

| | Put it here | Not here |
| --- | --- | --- |
| Mac | `/Users/you/Obsidian/My Wiki` (make an `Obsidian` folder in your home folder) | iCloud Drive, Desktop or Documents if they sync to iCloud |
| Windows | `C:\Vaults\My Wiki` (make a `Vaults` folder on C:) | Documents, Desktop or OneDrive. Keep the path short: Windows struggles past 260 characters |

Keep the rest of the unzipped kit somewhere too. You'll want `addons/` later.

### Step 5. Open it in Obsidian

1. Open Obsidian → **Open folder as vault** → choose `My Wiki`. If asked whether to trust the author, click **Trust author and enable plugins**.
2. **Install Dataview**, which draws the live tables:
   - **Settings** (⚙️ bottom left) → **Community plugins** → **Turn on community plugins**.
   - **Browse** → search `Dataview` → **Install** → **Enable**.
   - Back in Settings, click **Dataview** in the left list and switch on **Enable JavaScript queries**.
3. **Point templates at the right folder:**
   - **Settings → Core plugins** → switch on **Templates**.
   - **Settings → Templates** → **Template folder location** → `Admin/_templates`.

✅ **You should see** tables listing three example notes when you open **`+Home`** in the left sidebar. If you see blocks of code instead, Dataview isn't enabled. Redo part 2 above.

*Optional:* **Settings → Appearance → Themes → Manage** → install **AnuPpuccin** or **Minimal**. Also optional: install the **[Obsidian Web Clipper](https://obsidian.md/clipper)** browser extension and set it to save into `Clippings/`. That's the easiest way to feed the vault from the web.

### Step 6. Tell it what you care about

This is the one file you edit, and the most important five minutes of setup.

1. In Obsidian, open **`Admin/AGENTS.md`**.
2. Find **§0 About this vault** at the top, and replace each `TODO`:
   - **Owner:** your name.
   - **Focus / lens:** what every note is judged against. Be specific. "*A mid-sized UK water company's strategy team*" works far better than "*sustainability*".
   - **The "so what" question:** usually "*What does this mean for*" followed by your focus.
   - **Categories:** the default is PESTLE plus `Energy`. Rename `Energy` to your own extra category, or delete it. If you rename it, also rename the `10 Notes/Energy` folder and the `+Energy` page to match.
3. Leave the rest of the file alone, but read it once so you know what Claude has been told.

---

## Part 3 — Connect Claude (10 min)

### Step 7. Create a Claude Project for the vault

1. In the Claude desktop app, create a new **Project**, e.g. "My Wiki".
2. Open **`Admin/PROJECT-INSTRUCTIONS.md`** in Obsidian. Copy everything **below the line**, and paste it into the Project's **instructions**.
3. Connect your vault folder (`My Wiki`) so Claude can read and write it.

✅ **Test it.** In a conversation in that Project, ask:

> Read Admin/AGENTS.md and tell me, in three bullets, what you're allowed to write to.

It should mention `10 Notes/` and say it will ask before writing anywhere else. If it says it can't see the file, the folder isn't connected yet.

---

## Part 4 — Safety net (5 min)

### Step 8. Turn on nightly backups

Agents edit many notes at once. The backup records every change every night, so you can see exactly what changed and undo it.

1. Open a terminal **in your vault folder**:

   <details>
   <summary><b>Mac</b></summary>

   In the terminal, type `cd ` (with a space after it), **drag the `My Wiki` folder from Finder onto the terminal window**, and press **Return**.

   </details>

   <details>
   <summary><b>Windows</b></summary>

   In File Explorer, open `My Wiki`, right-click an empty space → **Open in Terminal**. On Windows 10, hold **Shift** while you right-click → **Open PowerShell window here**.

   </details>

2. Tell git who you are (first time only; use your own name and email):

   ```
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

3. Start the history and schedule the nightly backup:

   ```
   git init
   git add -A
   git commit -m "Starting point"
   python3 backup_vault.py --install
   ```

✅ **You should see** `✓ Nightly backup set for 21:00.`

- For a different time: `python3 backup_vault.py --install --time 22:30`
- To check it later: `python3 backup_vault.py --status`

<details>
<summary><b>Optional: also back up to GitHub</b></summary>

1. On GitHub, create a new repository and make it **Private**. Leave every box unticked.
2. Copy its URL, then in the terminal:

   ```
   git remote add origin https://github.com/YOUR-NAME/YOUR-REPO.git
   git push -u origin HEAD
   ```

   The first push asks you to sign in to GitHub. After that, the nightly backup pushes automatically. If a push ever fails, a note called **⚠️ Backup problem** appears in `Admin/` explaining what to do.

</details>

> ⚠️ **Never run `git clean` in your vault.** It permanently deletes any file git isn't tracking yet.

### Step 9. Run the setup checker

In the same terminal:

```
python3 check_setup.py
```

✅ **You should see** a list of ✓ ticks ending in **All good.** Anything marked ✗ comes with a → line telling you how to fix it. Fix it and run the checker again.

---

## Part 5 — First run (5 min)

### Step 10. Process the example clipping by hand

This shows you what the daily task will do, while you watch. In a conversation in your Claude Project, paste:

> Ingest `Clippings/Example clipping - Community energy schemes.md` following AGENTS.md §7. Tell me which notes you changed and why.

✅ **Check that:**

- [ ] It **updated** the existing heat pump note, rather than only creating a new one
- [ ] The new evidence line ends with a date like `*(2026-10-20)*`
- [ ] The `corroborations` count in that note's properties went up
- [ ] The clipping moved to `40 Archive/Processed captures/`, and `00 Inbox/_processing-log.md` has an entry

To see every change it made, run `git diff` in the terminal.

---

## Part 6 — Automate it (5 min)

### Step 11. Set up the scheduled tasks

Let Claude do this for you:

1. In the Claude app, start a new conversation **in your Project** with the vault folder connected.
2. Open **`Admin/prompts/00 Set up my scheduled tasks.md`** in Obsidian, copy everything below the line, and paste it in.
3. Answer Claude's questions. It asks which optional tasks you want, your email, and your time zone.
4. For each task it proposes, check the details and click **Schedule**.

**What you'll end up with:**

| Task | When | What it does | |
| --- | --- | --- | --- |
| **Daily ingest** | Daily 05:50 | Folds new captures into your notes | Core |
| **Your three** | Sundays 09:20 | Asks you to rate three notes. You reply in one line | Core |
| **Weekly lint** | Sundays 08:10 | Health check, with a short summary in the task's run | Core |
| Newsletter sync | Daily 05:10 | Copies your email newsletters into the inbox | Optional |
| Daily briefing | Weekdays 05:25 | A news round-up on your topics, into the inbox | Optional |
| Daily inspiration | Daily 07:40 | Emails you one random note, related news and five ideas | Optional |

If Claude can't create tasks from a conversation in your version of the app, it gives you each one ready to paste. Go to **Scheduled → New task → Set up manually**, and for each task enter the name, paste the prompt, choose your vault folder and set the time.

✅ **You should see** each task listed on the **Scheduled** page in the Claude app.

---

## Part 7 — Your first week

| When | What happens | What you do |
| --- | --- | --- |
| Every morning | The ingest processes anything new in `00 Inbox/` and `Clippings/` | Nothing. Check `00 Inbox/_processing-log.md` if you're curious |
| Whenever you read something good | — | Clip it, forward the newsletter, or write a note in `00 Inbox/` |
| Sunday morning | "Your three" emails you three questions | Open the **Your three** task's latest run in Claude and reply in one line, e.g. `1: 4 5 · 2: 5 2 – it's gas not nuclear · 3: skip` |
| Sunday | Weekly lint writes `Admin/_LINT.md` | Skim the top few items |
| After 1–2 weeks | — | Delete the notes marked **Example** in `10 Notes/`, `Clippings/` and `40 Archive/Processed captures/` |

**How to answer "Your three":** for each note, give two numbers from 1 to 5.

- **Importance: does it matter to you?** 5 top-level · 4 on someone's agenda now · 3 worth tracking · 2 background · 1 not relevant
- **Fit: does it match what you see?** 5 seen it first-hand · 4 broadly yes · 3 can't tell · 2 partly wrong · 1 wrong

Add a few words of reason whenever you like, especially if fit is 1 or 2. Your words go into the note in a box agents can never edit, and the agent must reply.

**Disagree any time:** tell Claude in your Project ("I don't buy the hydrogen note — costs aren't falling"), or type `#no` and a reason on any line of a note.

---

## Later

- **Weak-signals add-on:** once you have 50+ compiled notes, add the big-picture register. See [`addons/weak-signals`](addons/weak-signals).
- **Brief me on X:** ask your Project "Brief me on *topic*" (see `Admin/prompts/topic-briefing.md`).
- **Track what mattered:** when a note actually changes something you do, add one line to `Admin/Attention log.md`.

### Updating to a newer version of the kit

1. Download the new ZIP as in step 4.
2. Copy these from its `vault` folder into yours, replacing the old ones: all the `.py` scripts, `Admin/prompts/` and `Admin/_templates/`. **Never copy over `10 Notes/`, `00 Inbox/`, `40 Archive/` or `Admin/AGENTS.md`.**
3. For `AGENTS.md`, ask your Project: "*Merge the new rules from `<path to new>/vault/Admin/AGENTS.md` into my `Admin/AGENTS.md`. Keep my §0 and §8 exactly as they are, and show me what changed.*"
4. Run `python3 check_setup.py`.

### Removing it

- Delete the scheduled tasks on the Claude app's **Scheduled** page.
- Run `python3 backup_vault.py --remove` to stop the nightly backup.
- Your notes are plain Markdown files, and they stay yours.

---

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Anything at all | Run `python3 check_setup.py` first. It catches most setup problems |
| `+Home` shows code instead of tables | Dataview isn't installed or enabled (step 5) |
| `python3` / `py` not recognised | Mac: run `xcode-select --install`. Windows: re-run the Python installer with **Add python.exe to PATH** ticked, then open a new terminal |
| `git` not recognised (Windows) | Install git (step 2), then open a **new** terminal |
| Claude says it can't see the vault | Reconnect the vault folder to the Project. Check the folder isn't in OneDrive or iCloud |
| A morning's update didn't happen | Was the computer on, with the Claude app open, at 05:50? Check the task's run history on the **Scheduled** page |
| "Your three" never arrived | Check the **Your three** task's latest run on the **Scheduled** page. The question is there even if the email wasn't sent. Make sure Gmail is connected |
| New notes have the wrong structure | The ingest task's prompt has drifted. Check it starts by reading `Admin/AGENTS.md` |
| Lots of "Dead links" in the lint | Normal at first: links to notes that don't exist yet. Don't create empty pages for them |
| A **⚠️ Backup problem** note appeared | Do what it says. Usually: open a terminal in the vault, run `git push`, and sign in to GitHub again |
| `Unable to create '.git/index.lock'` | Wait a minute and try again. The nightly backup clears stale locks itself |
| A note won't open on Windows | Its name contains one of `: ? * " < > \|`. The setup checker lists these; rename them |

Still stuck? [Open an issue](../../issues/new/choose) and paste the output of `python3 check_setup.py`, with anything private removed.
