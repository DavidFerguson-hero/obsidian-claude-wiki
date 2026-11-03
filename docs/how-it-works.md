# How it works — and why it's built this way

## The idea

Most note-taking systems get worse as they grow. You capture more, link less, and the good ideas get buried. The fix this kit uses comes from Andrej Karpathy's "LLM wiki" idea: **treat your notes as a wiki that an AI compiles, not a pile you file.**

- You supply the raw material and your own thinking.
- Claude does the downstream work: merging new evidence into existing notes, counting and dating sources, linking, flagging contradictions.
- A rulebook (`AGENTS.md`) keeps Claude consistent across hundreds of runs.

## The layers

| Layer | Folder | Answers | Who writes it |
| --- | --- | --- | --- |
| **Inputs** | `00 Inbox/`, `Clippings/`, `05 Sources/` | "What did I read?" | You |
| **Knowledge base** | `10 Notes/` | "How strong is this idea, and what does it mean for my focus?" | Claude (plus your concept notes) |
| **Register** *(add-on)* | `60 Signals/` | "What's the big picture, and how is it moving?" | The weak-signals agent |
| **Archive** | `40 Archive/` | "What has already been processed?" | Claude, append only |

**The layers must not overlap.** A signal that restates a note adds nothing. An entity page that restates a note creates two versions of the truth. Each layer answers a different question.

## Two kinds of note

- **Compiled notes** are built from sources. They follow a fixed shape — *Core idea, Supporting evidence, Why this matters, Connections, Source* — and carry numbers that scripts can read: how many sources, how independent, how fresh, how strong.
- **Concept notes** are your own writing. Claude never creates them and never rewrites them. When new evidence touches one, your words move under `## Thoughts (original)` unchanged and the compiled structure is built around them.

## Evidence that can be checked

Every evidence line looks like this:

```markdown
- [Headline](https://source) — what it changes. *(2026-07-29)*
```

That one convention does a lot of work:

- **The date** lets scripts work out how fresh a note is and whether a theme is gaining or losing momentum.
- **The link** makes every claim traceable. An uncited claim is treated as a defect.
- **The domain** separates *corroboration* (how many articles) from *independence* (how many different publications). Ten links from one newsletter is one source, not ten — and independence drives confidence.

## Lessons learned the hard way

These rules are in `AGENTS.md` because each one fixed a real failure.

1. **Count evidence only in the evidence section.** Counting every link in a note once inflated a note's corroboration count from 21 to 35. Links in "Why this matters" are illustration, not proof.
2. **Never keep a second copy of the schema.** A note template quietly drifted from the rules and produced months of malformed notes while the health check reported all clear. The schema lives in one file; everything else points to it.
3. **Lint checks the body, not just the frontmatter.** A health check that only read the frontmatter called the vault healthy when only 3 of 145 compiled notes actually had the right sections.
4. **A processed capture must leave the inbox.** Flagging captures without moving them let the inbox fill with "done" items nobody could tell apart from new ones.
5. **"Assessed" doesn't prove a human judged it.** Agents wrote assessments that looked just like human ones. Agent-written assessments now carry an `UNREVIEWED` marker until you accept them.
6. **Assessments go stale silently.** Reasoning written against 11 sources reads the same when the note has 30. Each assessment is stamped with the counts it was written against, and lint flags when the evidence has moved on.
7. **Score on evidence, not excitement.** An early version scored notes higher for words like "breakthrough". A calmly worded, well-sourced claim should beat a breathless one.
8. **A signal is not a note.** Pointing a dashboard at every note produced 139 "signals" and was useless. About one signal per ten notes is the right ratio. The value is in what's left out.
9. **Every theme needs a tension.** The counter-force that might prove it wrong. Without one, a theme is just a category.
10. **Don't make the human a maintainer.** Anything that needs you to tag, promote or approve items will stop working the week you're busy. You feed it and you disagree with it. That's all.
11. **Track what you actually used.** A high score means the world is talking about something, not that it changed anything you did. The attention log is the only place that difference gets recorded.
12. **Back up with git, outside the agent.** Agents edit many files at once, so you need to see the diff. Run the commit from your Mac, not from inside Claude: a sandboxed git can leave lock files that jam the repository. And **never `git clean`** — it once destroyed a file in the original vault.

## What it doesn't do

- It won't decide what's worth reading. That's still your job, and it's the part that matters.
- It doesn't replace thinking. The so-what is only as good as the focus you write in `AGENTS.md` §0.
- It isn't a task manager, a journal, or a place for meeting notes.
