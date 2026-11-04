# Setup — about 30 minutes

Written for a Mac. Steps marked 🖥 use Terminal (Applications → Utilities → Terminal). Copy the commands as they are, swapping in your own folder path.

## What you need

- [Obsidian](https://obsidian.md) (free)
- The [Claude desktop app](https://claude.ai/download), on a paid plan that includes Projects and scheduled tasks
- Python 3 and git. 🖥 Check with `python3 --version` and `git --version`. If either is missing, macOS will offer to install the Command Line Tools — say yes.

---

## 1. Get the files

Click **Use this template → Create a new repository** on GitHub, or **Code → Download ZIP**.

Copy the `vault/` folder to where you want your vault to live and rename it, for example `~/Obsidian/My Wiki`.

> **Keep it out of iCloud Drive, Dropbox and OneDrive** if you can. Sync services and git can step on each other, and cloud-only files may be invisible to Claude. Back up with git instead (step 6).

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
```bash
cd ~/Obsidian/"My Wiki"        # your vault folder
python3 lint_wiki.py
```

You should see `✓ _LINT.md written` and a list of checks. Open `Admin/_LINT` in Obsidian — the example notes will show up in a few sections. That's expected.

## 6. Turn on nightly backups (strongly recommended)

Agents edit many notes at once. Git lets you see exactly what changed, and undo it.

🖥
```bash
cd ~/Obsidian/"My Wiki"
git init
git add -A
git commit -m "Starting point"
chmod +x install_autocommit.sh commit_vault.sh
./install_autocommit.sh
```

This commits the vault every night at 21:00. For a different time: `HOUR=22 MINUTE=30 ./install_autocommit.sh`.

Optional, for an off-machine copy: create a **private** GitHub repository and run `git remote add origin <its URL>` then `git push -u origin HEAD`. The nightly job will push from then on.

> ⚠️ **Never run `git clean` in your vault.** It permanently deletes any file git isn't tracking yet — including notes written since the last commit.

## 7. Try your first ingest by hand

In a chat in your Project, ask:

> Ingest `Clippings/Example clipping - Community energy schemes.md` following AGENTS.md §7. Tell me which notes you changed and why.

Then check:

- [ ] It **updated** the heat pump note rather than only creating a new one.
- [ ] The new evidence line ends with a date like `*(2026-10-20)*`.
- [ ] `corroborations` and `independent_sources` went up correctly.
- [ ] The clipping moved to `40 Archive/Processed captures/` and the processing log has an entry.

🖥 `git diff` shows every change.

## 8. Schedule it

Create these as scheduled tasks in the Claude app, from the prompts in [`prompts/`](prompts). Replace `PATH/TO/YOUR/VAULT` in each one.

| Task | When |
| --- | --- |
| Daily ingest | Every day, early morning |
| Weekly lint | Weekly |
| Daily briefing (optional) | Weekdays, before the ingest |

Keep the git autocommit **after** all of them.

## 9. Clear out the examples

After a week or two of real use, delete the files marked "Example" in `10 Notes/`, `Clippings/` and `40 Archive/Processed captures/`, and the example line in `Admin/Attention log.md`.

## 10. Use it

- **Feed it.** Clip articles, forward newsletters into `00 Inbox/`, write your own concept notes using the `Concept Note` template.
- **Ask it.** "Brief me on X" in your Project — see [`prompts/topic-briefing.md`](prompts/topic-briefing.md).
- **Tell it what mattered.** When a note actually changes something you do, add one line to `Admin/Attention log.md`. Over time this shows you which "strong" signals were noise.
- **Read the lint.** Weekly, look at the top of `Admin/_LINT.md`. The **Overdue assessment** list is the best use of ten minutes.

When you have 50+ compiled notes, consider the [weak-signals add-on](addons/weak-signals).

---

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `+Home` shows code instead of tables | Enable Dataview (step 2) |
| Claude says it can't see the vault | Give the Project access to the folder again; check the folder isn't cloud-only |
| `fatal: Unable to create '.git/index.lock': File exists` | 🖥 `rm .git/index.lock` (only when no git command is running). The nightly script clears it automatically |
| New notes have the wrong frontmatter | Your scheduled ingest prompt has drifted. Check it starts by reading `Admin/AGENTS.md` |
| Lint shows lots of "Dead links" | Normal at first — links to notes not written yet. Don't create empty pages to satisfy them |
| Push failed notification | 🖥 `cd` to the vault and run `git push` by hand to see the error — usually expired GitHub credentials |

Still stuck? [Open an issue](../../issues).
