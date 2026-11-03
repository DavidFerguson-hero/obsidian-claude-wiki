---
title: "+Signals"
type: moc
tags: ["moc", "signals"]
---

# 📡 Signals register

Syntheses **across** the knowledge base, grouped into [[+Themes|themes]]. Rules: [[SIGNALS]]. Feed: `signals.json` (run `python3 build_signals_json.py`).

## Run log
<!-- newest first; the weak-signals agent writes a few lines here each run -->
- 2026-10-01 — *example entry.* No themes changed. One signal proposed: [[SIG - Cheaper Than Forecast]].

## Active signals

```dataview
TABLE WITHOUT ID file.link AS "Signal", theme AS "Theme", strength AS "Strength", maturity AS "Maturity", impact AS "Impact", horizon AS "Horizon", last_updated AS "Updated"
FROM "60 Signals"
WHERE type = "signal" AND status != "retired"
SORT impact DESC
```

## Retired

```dataview
LIST FROM "60 Signals" WHERE type = "signal" AND status = "retired"
```
