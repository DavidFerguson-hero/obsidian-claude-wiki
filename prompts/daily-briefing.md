# Daily briefing (optional input feed)

This feeds the inbox — it does not touch the wiki. Schedule it *before* the daily ingest. Copy everything below the line into a scheduled task and edit the topics.

---

Search the web for the most significant news from the last 24 hours on these topics: TOPIC 1, TOPIC 2, TOPIC 3 ← replace these with your own.

Pick 5–10 items that would change how someone focused on FOCUS ← replace this thinks. Prefer original reporting and primary sources over commentary. Skip anything you cannot find a source URL for.

Write one Markdown file to `PATH/TO/YOUR/VAULT/00 Inbox/` ← replace this, named `YYYY-MM-DD Daily briefing.md` (today's date), with this frontmatter:

```yaml
---
title: "YYYY-MM-DD Daily briefing"
type: capture
created: YYYY-MM-DD
tags: ["briefing"]
---
```

For each item: a `##` headline, two or three sentences on what happened and why it matters, the publication date, and the source URL as a Markdown link.

Write only that one file. Do not edit anything else in the vault — the daily ingest will pick it up.
