# Set up my scheduled tasks

Use this instead of creating each scheduled task by hand. Claude asks you a few questions, fills in each prompt for you, and sets the tasks up.

**How:** in the Claude desktop app, make sure your vault folder is connected, start a new task or conversation, and paste everything below the line. Claude proposes each task; you check it and click **Schedule**.

If your Claude app can't create scheduled tasks from a conversation, Claude will give you each task's name, schedule and prompt ready to paste into **Scheduled → New task → Set up manually** instead.

---

Please set up the scheduled tasks for my Obsidian vault, using the prompt files in the vault's `Admin/prompts/` folder.

**First, find out what you need.**

1. Find my vault folder among the folders connected to this conversation — it's the one containing `Admin/AGENTS.md`. Tell me the full path you found. If no connected folder has it, stop and tell me to connect my vault folder first.
2. Read `Admin/AGENTS.md` §0. If it still contains `TODO`, stop and tell me to fill it in first (SETUP.md step 5).
3. Read every file in `Admin/prompts/`, including `README.md`. If `60 Signals/` exists in the vault, the weak-signals add-on is installed: also look for `weekly-weak-signals.md` in `Admin/prompts/`.
4. Ask me, in one message, with numbered questions:
   - Which **optional** tasks I want: daily briefing, newsletter sync, daily inspiration (and weak signals, if installed). Explain each in one line.
   - Anything the chosen tasks need: my email address (for daily inspiration), my briefing topics, my newsletter sender addresses.
   - My time zone, and whether the suggested times below suit me.

**Then set up each task** — the core ones always: **Daily ingest**, **Your three**, **Weekly lint**, plus the optional ones I chose.

For each task:
- Take the prompt text below the `---` line in its file, and fill in every `←` placeholder (vault path, email, topics, senders). Leave nothing marked `←`.
- Make sure the task runs with my vault folder, because every task reads or writes it.
- Use these default times unless I asked for others. They're in order on purpose, so each task's input is ready before it runs, and they finish before the nightly backup at 21:00:

  | Task | When |
  | --- | --- |
  | Newsletter sync | Daily 05:10 |
  | Daily briefing | Weekdays 05:25 |
  | Daily ingest | Daily 05:50 |
  | Daily inspiration | Daily 07:40 |
  | Weekly lint | Sundays 08:10 |
  | Weak signals | Sundays 08:35 |
  | Your three | Sundays 09:20 |

- Show me the name, schedule and filled-in prompt, and let me confirm it.

**Finally**, give me a short table of every task you set up and its schedule, and remind me in one line that my computer must be on with the Claude app open at those times, because the tasks work on files on my computer.

Don't change any notes while doing this. Don't run any of the tasks yet.
