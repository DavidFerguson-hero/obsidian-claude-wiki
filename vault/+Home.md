---
title: "+Home"
type: moc
tags: ["moc"]
---

# +Home

Router for the compiled wiki. Everything below is generated live by Dataview, so it cannot go stale.

Agents: read [[AGENTS]] before writing anything.

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

---

Also: [[Signal dashboard]] · [[Attention log]] · [[_LINT]]
