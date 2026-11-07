---
title: "+Home"
type: moc
tags: ["moc"]
---

# +Home

Router for the compiled wiki. Everything below is generated live by Dataview, so it cannot go stale.

Agents: read [[AGENTS]] (in `Admin/`) before writing anything.

---

## Categories

| | Category | What lives here |
|---|---|---|
| 💰 | [[+Economic]] | Markets, capital, investment, business models |
| ⚡ | [[+Energy]] | Your extra category — rename to suit your focus |
| 🌍 | [[+Environmental]] | Climate, carbon, nature |
| ⚖️ | [[+Legal]] | Regulation, standards, law |
| 🏛 | [[+Political]] | Policy, geopolitics, government |
| 👥 | [[+Social]] | Work, behaviour, demographics, culture |
| 🔬 | [[+Technological]] | AI, digital, materials, hardware |

---

<!-- Weak-signals add-on: paste the themes-and-signals map from 60 Signals/+Signals.md here. -->

## Well evidenced and important to you

Strong evidence *and* you rated it 4+ for importance in the weekly "Your three" review.

```dataview
TABLE WITHOUT ID
  file.link AS "Note", pestle AS "Category", importance AS "Imp", fit AS "Fit",
  signal_strength AS "Str", so_what AS "So what"
FROM "10 Notes"
WHERE type = "compiled" AND importance >= 4 AND signal_strength >= 5
SORT importance DESC, signal_strength DESC
```

### Where you disagreed

```dataview
TABLE WITHOUT ID file.link AS "Note", fit AS "Fit", reviewed AS "Rated"
FROM "10 Notes"
WHERE type = "compiled" AND fit AND fit <= 2
SORT reviewed DESC
```

## Strongest signals right now

```dataview
TABLE WITHOUT ID
  file.link AS "Note", pestle AS "Category", signal_strength AS "Str",
  independent_sources AS "Indep", horizon AS "Horizon", so_what AS "So what"
FROM "10 Notes"
WHERE type = "compiled" AND signal_strength
SORT signal_strength DESC
LIMIT 15
```

## Newest evidence

```dataview
TABLE WITHOUT ID file.link AS "Note", last_evidence AS "Newest", corroborations AS "Src"
FROM "10 Notes"
WHERE type = "compiled" AND last_evidence
SORT last_evidence DESC
LIMIT 10
```

## Near-term and well corroborated

Happening now or soon, with more than one independent source behind it.

```dataview
TABLE WITHOUT ID
  file.link AS "Note", pestle AS "Category", independent_sources AS "Indep", so_what AS "So what"
FROM "10 Notes"
WHERE type = "compiled" AND (horizon = "now" OR horizon = "near") AND independent_sources > 1
SORT independent_sources DESC, signal_strength DESC
```

---

## Quick checks

The full health check is [[_LINT]] (run `python3 lint_wiki.py`, or `py lint_wiki.py` on Windows). These are the live views.

### Single-source claims — treat with caution

```dataview
TABLE WITHOUT ID file.link AS "Note", pestle AS "Category", confidence AS "Conf", signal_strength AS "Str"
FROM "10 Notes"
WHERE type = "compiled" AND independent_sources <= 1
SORT signal_strength DESC
```

### Low confidence — review or retire

```dataview
TABLE WITHOUT ID file.link AS "Note", pestle AS "Category", confidence AS "Conf"
FROM "10 Notes"
WHERE type = "compiled" AND confidence < 0.5
SORT confidence ASC
```

### Marked stale

```dataview
LIST
FROM "10 Notes"
WHERE stale = true
```

### Date unknown

These notes have no recoverable `first_seen`, so freshness and momentum can't be worked out for them.

```dataview
TABLE WITHOUT ID file.link AS "Note", pestle AS "Category"
FROM "10 Notes"
WHERE type = "compiled" AND first_seen = "unknown"
```

---

## Concept notes waiting to be compiled

Your own notes convert to compiled only when new evidence touches them. This is a backlog, not a to-do list.

```dataview
TABLE WITHOUT ID length(rows) AS "Awaiting compile"
FROM "10 Notes"
WHERE type = "concept"
GROUP BY split(file.folder, "/")[1] AS Category
SORT length(rows) DESC
```

---

## Elsewhere in the vault

- `00 Inbox/`, `Clippings/` — what you feed in; ingest reads these, then archives them
- `05 Sources/` — immutable source material, never edited
- `20 Personal/` — yours, outside the wiki
- `40 Archive/` — processed captures and completed work
- `Admin/` — [[AGENTS]], templates, [[Signal dashboard]], [[Attention log]], [[_LINT]]
