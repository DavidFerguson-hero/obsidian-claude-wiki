# Setup — about 30 minutes

Works on **Mac** and **Windows** (and Linux). Where the two differ, both are shown. Steps marked 🖥 need a terminal.

## Opening a terminal in your vault folder

| | Mac | Windows |
| --- | --- | --- |
| Open a terminal **in the vault folder** | In Finder, right-click the vault folder → **New Terminal at Folder**. (If you don't see it: System Settings → Keyboard → Keyboard Shortcuts → Services → Files and Folders → tick **New Terminal at Folder**.) | In File Explorer, open the vault folder, right-click empty space → **Open in Terminal**. |
| Run Python | `python3` | `py` |

Every 🖥 command below assumes the terminal is already in your vault folder. Where you see `python3`, type `py` on Windows.

## What you need

- [Obsidian](https://obsidian.md) (free)
- The [Claude desktop app](https://claude.ai/download), on a paid plan that includes Projects and scheduled tasks
- **Python 3.8+** and **git**:

| | Mac | Windows |
| --- | --- | --- |
| Check | 🖥 `python3 --version` and `git --version` | 🖥 `py --version` and `git --version` |
| Install if missing | Running either command offers to install Apple's Command Line Tools — say yes. | Python: [python.org/downloads](https://www.python.org/downloads/) — tick **Add python.exe to PATH**. Git: [git-scm.com/download/win](https://git-scm.com/download/win), accept the defaults. Then close and reopen the terminal. |

---

## 1. Get the files

Click **Use this template → Create a new repository** on GitHub, or **Code → Download ZIP**.

Copy the `vault/` folder to where you want your vault and rename it. Keep the path short and **outside cloud-sync folders**:

| | Good place | Avoid |
| --- | --- | --- |
| Mac | `~/Obsidian/My Wiki` | iCloud Drive, Dropbox |
| Windows | `C:\Vaults\My Wiki` | **OneDrive** — Windows often puts Documents and Desktop inside OneDrive without telling you. Also avoid long paths: Windows struggles past 260 characters. |

Sync services and git step on each other, and cloud-only files can be invisible to Claude. Back up with git instead (step 6).

## 2. Open it in Obsidian

1. Obsidian → **Open folder as vault** → choose your folder.
2. Settings → **Community plugins** → turn them on → **Browse** → install and enable **Dataview**. In Dataview's own settings, switch on **Enable JavaScript queries** (needed for the signals map in the add-on).
3. Settings → **Core plugins** → **Templates** → set the template folder to `Admin/_templates`.
4. Optional: Settings → **Appearance** → **Themes** → **Manage** → install **AnuPpuccin** (the theme the original vault uses; **Minimal** also works well). The dashboards use the theme's own colours, so any theme is fine.
5. Optional: install the [Obsidian Web Clipper](https://obsidian.md/clipper) browser extension and set it to save into `Clippings/`. This is the easiest way to feed the vault.

Housekeeping files — `AGENTS.md`, templates, the attention log and the lint report — live in `Admin/`, so the top level stays tidy. Scripts stay in the vault root.

Open `+Home`. You should see tables with the example notes in them. If you see code blocks instead, Dataview isn't enabled.

## 3. Tell it what you care about

Open `Admin/AGENTS.md` and fill in **§0 About this vault**:

- **Owner** — your name.
- **Focus / lens** — what every note is judged against. Be specific: "a mid-sized UK water company's strategy team" works much better than "sustainability".
- **Categories** — the default is PESTLE plus `Energy`. Rename `Energy` to your own extra category, or delete it. If you rename it, rename the folder in `10 Notes/` and its `+Energy` index page to match.

That's the only part of `AGENTS.md` you need to edit. Read the rest once so you know what Claude has been told.

## 4. Create a Claude Project

1. In the Claude desktop app, create a new **Project** for the vault.
2. Open `Admin/PROJECT-INSTRUCTIONS.md`, copy everything below the line, and paste it into the Project's instructions.
3. Give the Project access to your vault folder.

Test it: in a chat in that Project, ask *"Read Admin/AGENTS.md and tell me, in three bullets, what you're allowed to write to."* It should name `10 Notes/` and mention asking before writing anywhere else.

## 5. Check the scripts run

🖥
```
python3 lint_wiki.py
```

You should see `✓ _LINT.md written` and a list of checks. Open `Admin/_LINT` in Obsidian — the example notes will show up in a few sections. That's expected.

## 6. Turn on nightly backups (strongly recommended)

Agents edit many notes at once. Git lets you see exactly what changed, and undo it.

🖥 First time only — tell git who you are:
```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Then:
```
git init
git add -A
git commit -m "Starting point"
python3 backup_vault.py --install
```

That backs the vault up every night at 21:00 — using launchd on a Mac and Task Scheduler on Windows. For a different time: `python3 backup_vault.py --install --time 22:30`. To check it: `python3 backup_vault.py --status`.

Optional, for an off-machine copy: create a **private** GitHub repository, then run `git remote add origin <its URL>` and `git push -u origin HEAD`. The nightly backup pushes from then on. If a push ever fails, a note called **⚠️ Backup problem** appears in `Admin/` explaining what to do.

> ⚠️ **Never run `git clean` in your vault.** It permanently deletes any file git isn't tracking yet — including notes written since the last commit.

## 7. Check everything

🖥
```
python3 check_setup.py
```

It checks Python, git, Dataview, the folders, your §0 settings, the backup schedule, and Windows-unsafe file names, and tells you in plain words what to fix. Run it again any time something seems off.

## 8. Try your first ingest by hand

In a chat in your Project, ask:

> Ingest `Clippings/Example clipping - Community energy schemes.md` following AGENTS.md §7. Tell me which notes you changed and why.

Then check:

- [ ] It **updated** the heat pump note rather than only creating a new one.
- [ ] The new evidence line ends with a date like `*(2026-10-20)*`.
- [ ] `corroborations` and `independent_sources` went up correctly.
- [ ] The clipping moved to `40 Archive/Processed captures/` and the processing log has an entry.

🖥 `git diff` shows every change.

## 9. Schedule it

Create these as scheduled tasks in the Claude app, from the prompts in [`prompts/`](prompts). Replace `PATH/TO/YOUR/VAULT` in each one.

| Task | When |
| --- | --- |
| Daily ingest | Every day, early morning |
| Your three | Weekly, e.g. Sunday morning — turn on push notifications |
| Weekly lint | Weekly |
| Daily briefing (optional) | Weekdays, before the ingest |

Keep the nightly backup **after** all of them, so each day's agent changes land in one reviewable commit.

## 10. Clear out the examples

After a week or two of real use, delete the files marked "Example" in `10 Notes/`, `Clippings/` and `40 Archive/Processed captures/`, and the example line in `Admin/Attention log.md`.

## 11. Use it

- **Feed it.** Clip articles, forward newsletters into `00 Inbox/`, write your own concept notes using the `Concept Note` template.
- **Answer "Your three".** Once a week, two numbers per note, one line. Disagreeing is the most useful thing you can do — it's how the vault learns what you know.
- **Ask it.** "Brief me on X" in your Project — see [`prompts/topic-briefing.md`](prompts/topic-briefing.md).
- **Disagree any time.** Tell Claude in chat ("I don't buy the hydrogen note — costs aren't falling"), or type `#no` and a reason on any line of a note.
- **Tell it what mattered.** When a note actually changes something you do, add one line to `Admin/Attention log.md`.
- **Read the lint.** Weekly, look at the top of `Admin/_LINT.md`.

When you have 50+ compiled notes, consider the [weak-signals add-on](addons/weak-signals).

---

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Anything at all | 🖥 `python3 check_setup.py` first — it catches most setup problems |
| `+Home` shows code instead of tables | Enable Dataview (step 2) |
| `python3` / `py` not recognised | Windows: reinstall Python with **Add python.exe to PATH** ticked, then reopen the terminal. Mac: run `xcode-select --install` |
| Claude says it can't see the vault | Give the Project access to the folder again; check the folder isn't cloud-only (OneDrive / iCloud) |
| `fatal: Unable to create '.git/index.lock': File exists` | Wait a minute and retry; the nightly backup clears stale locks automatically. If it persists, delete `.git/index.lock` while no git command is running |
| New notes have the wrong frontmatter | Your scheduled ingest prompt has drifted. Check it starts by reading `Admin/AGENTS.md` |
| Lint shows lots of "Dead links" | Normal at first — links to notes not written yet. Don't create empty pages to satisfy them |
| A **⚠️ Backup problem** note appeared | Follow what it says — usually 🖥 `git push` to see the error, then re-sign in to GitHub |
| Windows: a note won't open or sync | Its name probably contains `: ? * " < > |`. `check_setup.py` lists them — rename them |

Still stuck? [Open an issue](../../issues).
