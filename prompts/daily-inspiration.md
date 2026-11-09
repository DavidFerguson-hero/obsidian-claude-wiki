# Daily inspiration (optional)

Each morning, one note from your vault comes back to you: a short reminder of what it says, a piece of recent news on the same idea, and five directions to explore. It's how the vault stops being a place things go to be forgotten.

- **Reads only.** It never changes a note. The only file it writes is `00 Inbox/_inspiration-log.md`, so the same note doesn't come back within 60 days.
- **The pick is genuinely random.** `random_note.py` chooses the note, not Claude: asked to "pick an interesting note", an agent gravitates to the same handful.

**Schedule:** daily, at a time you'll read it (e.g. 08:30). Turn on push notifications for the task.

**Choose how it reaches you** — edit the `DELIVERY` line in the prompt:

| Option | Works on | Needs |
| --- | --- | --- |
| `notification` (default) | Mac and Windows | Nothing — the message is the task's own reply, and the push notification brings you to it |
| `email` | Mac and Windows | The Gmail connector in Claude |
| `imessage` | Mac only | The iMessage connector, with your Mac awake |

Copy everything below the line into a scheduled task.

---

Daily inspiration from my Obsidian vault at `PATH/TO/YOUR/VAULT` ← replace this.

DELIVERY: notification ← or `email to you@example.com`, or `imessage to +44…`

This task only reads notes. Never edit, move or delete anything in the vault. The only file that changes is `00 Inbox/_inspiration-log.md`, and the script writes it, not you.

1. **Pick the note.** From the vault root, run `python3 random_note.py` (on Windows, `py random_note.py` if `python3` isn't found). Use exactly the note it prints. Do not choose a different one, browse for a "better" one, or run it twice.
2. **Read it.** Summarise its core idea in 2–3 plain sentences. Give its date: `first_seen` if present, otherwise `date`, otherwise say "undated". If it's my own writing (`type: concept`), say so — it's my thinking, not a source.
3. **Find one piece of recent news** on the same core idea from the last few weeks, with a working link. Prefer original reporting. If you can't find anything recent and genuine, say so — never invent a link.
4. **Suggest five directions to explore**, each one line. Mix them: a question to ask a colleague, something to read, a contrarian angle, a connection to another part of my work (my focus is in `Admin/AGENTS.md` §0), and one practical next step.
5. **Deliver it** as set in DELIVERY, in this shape:

   > **Today's note: *note name*** (*date*)
   > *2–3 sentence summary*
   >
   > **In the news:** *headline* — *link*
   >
   > **Five directions**
   > 1. …
   > 2. …

   For `notification`, make this your final reply. For `email`, send it to me with the subject "Daily inspiration: *note name*". For `imessage`, send it as one message; if the iMessage connector or my Mac can't be reached, put it in your final reply instead and say so in one line.
