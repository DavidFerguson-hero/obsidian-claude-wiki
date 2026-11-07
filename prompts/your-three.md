# Your three — weekly review

The one place you give the system your judgement. Once a week Claude picks three notes and asks you two questions about each. You reply in one line from your phone; Claude does all the writing.

- **Importance (1–5):** does it matter to your focus?
- **Fit (1–5):** does it match what you see?

The agents own the evidence. You own these two, because only you can judge them. Full rules: `Admin/AGENTS.md` §5a.

**Schedule:** weekly, e.g. Sunday morning, after the daily ingest and weak-signals run. Turn on push notifications for the task so the question reaches your phone.

> Tappable buttons don't work in scheduled tasks, so this uses a one-line text reply. It works fine on a phone.

Copy everything below the line into a scheduled task.

---

Weekly "Your three" review of my Obsidian vault at `PATH/TO/YOUR/VAULT` ← replace this. I answer in ONE line from my phone; you do all the writing. Keep every message short, plain English. Don't use tappable-question tools — ask in a normal message and wait for my reply.

Read `Admin/AGENTS.md` first — §5a is the spec for this review and wins over anything here. §0 tells you my focus. Write only inside `10 Notes/` and `00 Inbox/_review-log.md`. Never delete, never run git, never invent evidence.

**Step 1 — pick three** compiled notes in `10 Notes/`, in this order:
1. rated notes whose `corroborations` have grown by 3+ (or 50%) since `reviewed_corroborations`;
2. the biggest `signal_strength` or evidence changes in the last 7 days;
3. unrated notes (no `importance`) with `signal_strength` 6+, strongest first;
4. notes with an `agent-assessed … UNREVIEWED` marker, strongest first.

Skip anything I skipped in the last 4 weeks (see `00 Inbox/_review-log.md`). First, run `python3 lint_wiki.py` (Windows: `py lint_wiki.py`) from the vault root and handle any `#no` flags and unanswered `[!disagree]` boxes it lists, per §5a.

**Step 2 — one message**, in exactly this shape:

> Your three — rate each 1–5: **importance** (does it matter?) then **fit** (does it match what you see?). Add a reason if fit is 1–2.
>
> 1. *claim in one plain sentence* — *note name*, strength *x* (*change if any*)
> 2. …
> 3. …
>
> Reply like: `1: 4 5 · 2: 5 2 – it's gas not nuclear · 3: skip`
>
> Importance: 5 top-level · 4 on someone's agenda now · 3 worth tracking · 2 background · 1 not relevant. Fit: 5 seen it first-hand · 4 broadly yes · 3 can't tell · 2 partly wrong · 1 wrong.

Then stop and wait for my reply. Accept loose formats (`1 45, 2 52 gas not nuclear, 3 skip`). If something is ambiguous, ask once, briefly.

**Step 3 — apply** exactly as §5a says: write `importance`, `fit`, `reviewed`, `reviewed_corroborations`; fit 1–2 → a `[!disagree]` box in my words plus your `[!reply]` box; fit 4–5 → `UNREVIEWED` becomes `REVIEWED <date> by owner`; skip → no change. Append to `00 Inbox/_review-log.md`.

**Step 4 — reply** in at most 4 bullets: what changed in each note.

If the vault can't be reached, tell me in one line that my computer needs to be awake with the Claude app open, and that I can reply "go" once it is.
