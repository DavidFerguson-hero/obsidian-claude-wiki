---
title: "+Themes"
type: moc
tags: ["moc", "signals"]
---

# 🧭 Themes

Patterns found by reading **across** signals. Each names a dynamic several signals point to at once. The weak-signals agent challenges them every run — merging, splitting, retiring and proposing — and records why.

Each theme carries a **tagline**, **description**, **insight** and **tension**. The tension is the most valuable field: a theme without one is just a category.

```dataview
TABLE WITHOUT ID file.link AS "Theme", tagline AS "Claim", status AS "Status", last_reviewed AS "Reviewed"
FROM "60 Signals/Themes"
WHERE type = "theme"
SORT theme_id ASC
```
