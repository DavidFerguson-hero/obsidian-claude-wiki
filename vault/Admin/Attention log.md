---
title: "Attention log"
type: log
tags: ["meta"]
---

# 👁 Attention log

The one thing the vault cannot work out for itself: **which signals actually changed what you did.**

`signal_strength` measures how much the world is talking about something. It says nothing about whether it was useful to you. A note can score 9 because twenty articles mention it — without ever altering a decision. This log is the only place that distinction gets recorded.

## How to use it

Add one line when a signal earns its keep. Nothing else.

```
- 2026-08-04 · [[Signal note name]] — where it was used
```

That's the whole format. Date, link, a few words. If it takes longer than ten seconds it won't happen, so don't write more than that.

**What counts as "used":** cited in a paper or deck, shaped an argument in a meeting, changed a plan, prompted a conversation worth having, or made you go and read the sources. Merely finding it interesting doesn't count — that's what `signal_strength` already captures.

Run `python3 apply_attention.py` afterwards (or let the weekly lint prompt you) to write `last_used` back into the notes so Dataview can see it.

---

## Log

<!-- newest at the top -->

- 2026-10-01 · [[Heat pump installation costs falling faster than forecast]] — example entry, delete once you have real ones

---

## What this is telling you

### Signals that have earned their keep

```dataview
TABLE WITHOUT ID
  file.link AS "Signal", signal_strength AS "Str", last_used AS "Last used", used_count AS "Times", so_what AS "So what"
FROM "10 Notes"
WHERE type = "compiled" AND last_used
SORT last_used DESC
```

### High score, never used

The interesting column. If a signal sits here for months, either it is genuinely background noise that the scoring overrates, or you are missing something. Both are worth knowing.

```dataview
TABLE WITHOUT ID
  file.link AS "Signal", pestle AS "Domain", signal_strength AS "Str", corroborations AS "Src"
FROM "10 Notes"
WHERE type = "compiled" AND signal_strength >= 6 AND !last_used
SORT signal_strength DESC
LIMIT 20
```

### Used, but scored low

The opposite failure, and the more useful one. If something you keep reaching for scores badly, the scoring method is wrong — not your judgement. Ask Claude to adjust it.

```dataview
TABLE WITHOUT ID
  file.link AS "Signal", signal_strength AS "Str", used_count AS "Times used", corroborations AS "Src"
FROM "10 Notes"
WHERE type = "compiled" AND last_used AND signal_strength < 5
SORT used_count DESC
```

### Where your attention goes by domain

```dataview
TABLE WITHOUT ID
  length(rows) AS "Signals used", sum(rows.used_count) AS "Total uses"
FROM "10 Notes"
WHERE type = "compiled" AND last_used
GROUP BY pestle AS Domain
SORT sum(rows.used_count) DESC
```

---

Related: [[Signal dashboard]] · [[+Home]] · [[AGENTS]]
