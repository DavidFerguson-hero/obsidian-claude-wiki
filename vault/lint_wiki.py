#!/usr/bin/env python3
"""
Wiki lint — the reassessment loop
=================================
AGENTS.md §7 specifies a lint operation. This is it.

It REPORTS. It never edits a note. Everything it finds is a judgement call
for the vault owner or for an agent working under AGENTS.md, and silently "fixing"
a contradiction is exactly how a wiki drifts away from its sources.

Writes `Admin/_LINT.md` (or `_LINT.md` in the vault root if there is no Admin folder). Run:

    python3 lint_wiki.py

Checks:
  1. Quiet signals      — strong, but no new evidence for a long time
  2. Promotion queue    — derived notes now well-corroborated enough to deserve judgement
  3. Uncited claims     — <!-- UNCITED --> markers, and compiled notes with no cited URL at all
  4. Orphans            — nothing links to them
  5. Dead links         — [[targets]] with no matching file
  6. Contradiction candidates — note pairs that share topic vocabulary but disagree in direction
  7. Schema drift       — compiled notes missing required fields, or stale-flagged
  8. Overdue assessment — highest-strength notes still on `so_what: not yet assessed`
  9. Attention gap      — high-strength signals never recorded as used (loop 4)
"""

import re, sys, json, collections
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

ROOT   = Path(__file__).parent
NOTES  = ROOT / "10 Notes"
ADMIN  = ROOT / "Admin" if (ROOT / "Admin").is_dir() else ROOT
OUT    = ADMIN / "_LINT.md"
TODAY  = date.today()

REQUIRED = ["title","type","pestle","confidence","first_seen","first_seen_basis","last_evidence",
            "corroborations","independent_sources","signal_strength","strength_basis","horizon",
            "so_what","stale"]

# AGENTS.md §2 — the section set every compiled note must carry.
# Kept here rather than inferred from the corpus on purpose: the corpus is the
# thing being measured. If this list and AGENTS.md §2 ever disagree, AGENTS.md wins.
REQUIRED_SECTIONS = ["Core idea", "Supporting evidence", "Why this matters",
                     "Connections", "Source"]

# Headings that mean "Why this matters" under another name. A note carrying one
# of these needs a rename, not new prose — worth separating from the notes where
# the thinking genuinely has not been done.
MERGEABLE = {"Implications", "Implication", "Key insight", "Key nuance",
             "What this means", "Implications for innovation strategy",
             "Implications for strategy"}

# AGENTS.md §5 — required only where a human judged the score.
ASSESSED_BASIS = "assessed"

# AGENTS.md §4 — `sources:` is a list of resolvable paths. The pre-migration
# `source:` string is encounter-provenance in the wrong field; it belongs in
# the `## Source` body section.
LEGACY_SOURCE_KEY = "source"

# words that signal direction; a pair of notes using the same nouns with opposite
# direction words is a *candidate* contradiction, never a confirmed one.
UP   = {"accelerat","increas","surg","grow","rising","expand","outpac","record","boom"}
DOWN = {"slow","declin","fall","stall","retreat","reversal","delay","shrink","cut","pause"}


def parse(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\n(.*?)\n---", t, flags=re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).split("\n"):
        km = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if km:
            v = km.group(2).strip()
            if v.startswith('"') and v.endswith('"') and len(v) > 1:
                v = v[1:-1]
            fm[km.group(1)] = v
    body = t[m.end():]
    return {"path": p, "rel": str(p.relative_to(ROOT)), "name": p.stem, "fm": fm, "body": body}


def num(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def days_since(s):
    try:
        return (TODAY - datetime.strptime(s, "%Y-%m-%d").date()).days
    except (TypeError, ValueError):
        return None


def evidence_block(body):
    m = re.search(r"^##\s*Supporting evidence\s*$(.*?)(?=^##\s|\Z)", body, flags=re.S | re.M)
    return m.group(1) if m else ""


def main():
    if not NOTES.exists():
        print(f"✗ {NOTES} not found"); return 1

    notes = [n for n in (parse(p) for p in sorted(NOTES.rglob("*.md"))) if n]
    comp  = [n for n in notes if n["fm"].get("type") == "compiled"]
    print(f"  {len(notes)} notes, {len(comp)} compiled")

    # link graph across the whole vault
    all_names = {p.stem for p in ROOT.rglob("*.md") if ".git" not in str(p)}
    all_files = {p.name for p in ROOT.rglob("*") if p.is_file() and ".git" not in str(p)}
    inbound = collections.Counter()
    dead = collections.defaultdict(list)
    for n in notes:
        for m in re.finditer(r"!?\[\[([^\]|#]+)", n["body"]):
            tgt = m.group(1).strip()
            if tgt in all_names or tgt in all_files:
                inbound[tgt] += 1
            else:
                dead[n["rel"]].append(tgt)

    L = []  # report sections

    # 1 ── quiet signals
    quiet = []
    for n in comp:
        d = days_since(n["fm"].get("last_evidence", ""))
        s = num(n["fm"].get("signal_strength"))
        if d is not None and s >= 5 and d > 90:
            quiet.append((d, s, n))
    quiet.sort(key=lambda x: -x[0])
    if quiet:
        L.append(("Quiet signals", "Strength 5+, but no new evidence in over 90 days. Either the story stopped moving, or the vault stopped watching. Worth deciding which.",
                  [f"`{d}d` · **{s}** · [[{n['name']}]] — last evidence {n['fm'].get('last_evidence')}" for d, s, n in quiet[:20]]))
    else:
        # nothing has crossed the threshold yet — show the freshness tail instead,
        # so an empty check does not read as false reassurance
        tail = sorted(((days_since(n["fm"].get("last_evidence", "")), num(n["fm"].get("signal_strength")), n)
                       for n in comp if num(n["fm"].get("signal_strength")) >= 5
                       and days_since(n["fm"].get("last_evidence", "")) is not None),
                      key=lambda x: -x[0])[:6]
        L.append(("Quiet signals", "Nothing has gone quiet yet — no strength-5+ signal has been silent for 90 days. Freshness tail shown instead, so this section is informative rather than an empty tick.",
                  [f"`{d}d` · **{s}** · [[{n['name']}]]" for d, s, n in tail]))

    # 2 ── promotion queue
    promo = [n for n in comp
             if n["fm"].get("strength_basis") == "derived"
             and (num(n["fm"].get("independent_sources")) >= 2
                  or num(n["fm"].get("signal_strength")) >= 4.5)]
    promo.sort(key=lambda n: (-num(n["fm"].get("independent_sources")), -num(n["fm"].get("signal_strength"))))
    L.append(("Ready for judgement", "Derived notes with either 2+ independent sources or strength 4.5+. Arithmetic has taken these as far as it can — they have earned a real `so_what` and `horizon`. (Threshold is 2, not 4, because most young notes cite a single domain; a higher gate would surface almost nothing.)",
              [f"**{num(n['fm'].get('signal_strength'))}** · {n['fm'].get('independent_sources')} indep · [[{n['name']}]]" for n in promo[:20]]))

    # 3 ── uncited
    unc = [n for n in comp if "<!-- UNCITED -->" in n["body"]]
    nourl = [n for n in comp
             if not re.search(r"https?://", evidence_block(n["body"]))
             and n["fm"].get("strength_basis") != "curated"]
    L.append(("Uncited claims", "AGENTS.md §6: an uncited claim in a compiled note is a defect. `curated` notes are excluded — they are known to lack sources.",
              [f"[[{n['name']}]] — explicit UNCITED marker" for n in unc] +
              [f"[[{n['name']}]] — no URL anywhere in Supporting evidence" for n in nourl[:15]]))

    # 4 ── orphans
    orph = [n for n in comp if inbound[n["name"]] == 0]
    orph.sort(key=lambda n: -num(n["fm"].get("signal_strength")))
    L.append(("Orphans", "Nothing links to these. A strong orphan is usually a missing `## Connections` entry somewhere else, not a bad note.",
              [f"**{num(n['fm'].get('signal_strength'))}** · [[{n['name']}]]" for n in orph[:20]]))

    # 5 ── dead links
    flat = [(src, t) for src, ts in dead.items() for t in ts]
    top = collections.Counter(t for _, t in flat).most_common(15)
    L.append(("Dead links", f"{len(flat)} unresolved link instances across {len(dead)} notes. Most are missing image attachments or genuinely absent concepts — do not mass-create pages to satisfy them.",
              [f"`{c}×` {t}" for t, c in top]))

    # 6 ── contradiction candidates
    def topic_words(n):
        txt = (n["fm"].get("title", "") + " " + n["body"][:1500]).lower()
        return {w for w in re.findall(r"[a-z]{6,}", txt)}
    def direction(n):
        txt = n["body"][:2500].lower()
        u = sum(txt.count(w) for w in UP)
        d = sum(txt.count(w) for w in DOWN)
        return (u - d) / max(u + d, 1)
    strong = [n for n in comp if num(n["fm"].get("signal_strength")) >= 5]
    cands = []
    for i, a in enumerate(strong):
        wa, da = topic_words(a), direction(a)
        for b in strong[i + 1:]:
            if a["fm"].get("pestle") != b["fm"].get("pestle"):
                continue
            wb, db = topic_words(b), direction(b)
            overlap = len(wa & wb) / max(min(len(wa), len(wb)), 1)
            if overlap > 0.34 and abs(da - db) > 0.85:
                cands.append((round(overlap, 2), round(da - db, 2), a, b))
    cands.sort(key=lambda x: -x[0])
    L.append(("Contradiction candidates", "Same domain, heavily overlapping vocabulary, opposite directional language. **These are candidates, not findings** — the heuristic is crude and most will be complementary rather than contradictory. Worth a glance, nothing more.",
              [f"overlap `{o}` · [[{a['name']}]] ⟷ [[{b['name']}]]" for o, dd, a, b in cands[:10]]))

    # 7 ── schema drift (frontmatter fields)
    drift = []
    for n in comp:
        missing = [k for k in REQUIRED if k not in n["fm"]]
        if missing:
            drift.append(f"[[{n['name']}]] — missing `{', '.join(missing)}`")
    staled = [f"[[{n['name']}]]" for n in comp if n["fm"].get("stale") == "true"]
    L.append(("Schema drift and stale flags", "Missing fields usually mean a note was written by something that has not read AGENTS.md.",
              drift[:15] + [f"{s} — flagged `stale: true`" for s in staled]))

    # 7b ── section drift (body structure, AGENTS.md §2)
    # Frontmatter conformance says nothing about whether the note is actually
    # shaped like a compiled note. This checks the body.
    #
    # Split deliberately into two lists. A note that already says the right thing
    # under the wrong heading needs a rename; a note that never said it needs
    # someone to think. Lumping them together makes 115 notes look like one job
    # when 19 are mechanical and ~96 are judgement.
    sec_drift, renames = [], []
    for n in comp:
        heads = [h.strip() for h in re.findall(r"^##\s+(.+?)\s*$", n["body"], flags=re.M)]
        missing = [h for h in REQUIRED_SECTIONS if h not in heads]
        alias = [h for h in heads if h in MERGEABLE]
        if alias:
            renames.append(f"[[{n['name']}]] — `## {alias[0]}`" +
                           (" → merge into existing `## Why this matters`"
                            if "Why this matters" in heads else " → rename to `## Why this matters`"))
        if missing:
            # a note whose only gap is covered by an alias is a rename, not a hole
            if missing == ["Why this matters"] and alias:
                continue
            sec_drift.append((len(missing), f"[[{n['name']}]] — missing `## {'`, `## '.join(missing)}`"))
    sec_drift.sort(key=lambda x: -x[0])
    L.append(("Section drift", f"AGENTS.md §2: every compiled note carries `## Core idea`, `## Supporting evidence`, `## Why this matters`, `## Connections`, `## Source`. {len(sec_drift)} of {len(comp)} compiled notes have a genuine gap (notes needing only a rename are listed separately below). Worst offenders first. **Do not bulk-generate the missing sections** — an invented 'why this matters' is worse than an absent one. A newly written note appearing here means an agent has not read AGENTS.md.",
              [s for _, s in sec_drift[:15]]))

    L.append(("Heading renames — mechanical", f"{len(renames)} notes say the right thing under a heading the schema no longer uses (`## Implications` and friends belong in `## Why this matters`). These need a rename or a body merge, not new thinking — the cheapest conformance work in the vault.",
              renames[:20]))

    # 7c ── signal assessment, required only where a human judged the score (§5)
    no_assess = []
    for n in comp:
        if n["fm"].get("strength_basis") != ASSESSED_BASIS:
            continue
        if not re.search(r"^##\s+Signal assessment\s*$", n["body"], flags=re.M):
            no_assess.append((num(n["fm"].get("signal_strength")), f"**{num(n['fm'].get('signal_strength'))}** · [[{n['name']}]]"))
    no_assess.sort(key=lambda x: -x[0])
    L.append(("Assessed without reasoning", "AGENTS.md §5: `## Signal assessment` is required where `strength_basis: assessed` — a human set the score, so there is reasoning worth recording. Without it nobody can later tell whether an 8.4 was earned or guessed. `derived` notes are correctly excluded: the score is arithmetic and there is nothing to show.",
              [s for _, s in no_assess[:15]]))

    # 7c-ii ── agent-written assessments the owner has not yet confirmed
    # An assessment written by an agent from the note's own evidence is a
    # derived judgement wearing the clothes of a human one. Marked at write
    # time and surfaced here until the owner removes the marker, so the vault never
    # silently claims their judgement for reasoning they have not seen.
    unrev = []
    for n in comp:
        if "UNREVIEWED" in n["body"] and "agent-assessed" in n["body"]:
            unrev.append((num(n["fm"].get("signal_strength")),
                          f"**{num(n['fm'].get('signal_strength'))}** · [[{n['name']}]]"))
    unrev.sort(key=lambda x: -x[0])
    L.append(("Agent-assessed, awaiting your review", "Reasoning written by an agent from the note's own evidence, not by you. **Read it, then either delete the `<!-- agent-assessed … UNREVIEWED -->` comment to accept, or rewrite the section.** Until the marker goes, treat the score as unconfirmed.",
              [s for _, s in unrev[:20]]))

    # 7c-iii ── assessments overtaken by their own evidence
    #
    # The failure this catches: an assessment written against 11 sources still
    # sitting there when the note has 30. It reads as current — nothing about it
    # looks stale — but the reasoning was formed on a third of the evidence.
    # Ordinary staleness checks watch dates; this watches whether the *grounds*
    # of the judgement have moved. Every assessment carries an `assessed-at`
    # stamp of the counts it was written against, so the drift is computable
    # rather than guessed.
    overtaken = []
    for n in comp:
        m = re.search(r"<!--\s*assessed-at:\s*corroborations=(\S+)\s+independent_sources=(\S+)\s+"
                      r"last_evidence=(\S+)\s*-->", n["body"])
        if not m:
            continue
        was_c, was_i, was_d = num(m.group(1)), num(m.group(2)), m.group(3)
        now_c, now_i = num(n["fm"].get("corroborations")), num(n["fm"].get("independent_sources"))
        now_d = n["fm"].get("last_evidence", "")
        reasons = []
        # Independence moving is the one that should force a re-read: it is what
        # §5 says drives the score, and one new domain can change a "single
        # publication" caveat into a corroborated claim.
        if now_i > was_i:
            reasons.append(f"independent sources {was_i:g}→{now_i:g}")
        # Volume matters at a threshold, not per item — a note gaining 3 entries
        # is normal ingest; gaining 50% more is a different evidence base.
        if was_c and now_c >= was_c * 1.5:
            reasons.append(f"corroborations {was_c:g}→{now_c:g}")
        if now_d and was_d != "?" and now_d > was_d:
            reasons.append(f"new evidence since ({was_d} → {now_d})")
        if reasons:
            sev = (now_i - was_i) * 2 + (now_c - was_c) / max(was_c, 1)
            overtaken.append((sev, f"[[{n['name']}]] — {'; '.join(reasons)}"))
    overtaken.sort(key=lambda x: -x[0])
    L.append(("Assessments overtaken by evidence", "The assessment was written against a smaller evidence base than the note now has. **This is the check that keeps assessments honest as notes grow** — reasoning formed on 11 sources reads exactly the same when the note reaches 30, and nothing else here would notice. A new *independent domain* is the trigger worth acting on: §5 makes independence the dominant factor, so one new domain can turn a 'single publication' caveat into a corroborated claim. Re-read the assessment, revise if the reasoning has moved, and update the `assessed-at` stamp. Growth in raw corroborations alone is flagged only past 1.5x, since ordinary ingest adds entries constantly.",
              [s for _, s in overtaken[:15]]))

    # 7d ── legacy source key
    legacy = [f"[[{n['name']}]]" for n in comp
              if LEGACY_SOURCE_KEY in n["fm"] and "sources" not in n["fm"]]
    L.append(("Legacy `source:` key", "AGENTS.md §4: `sources:` is a list of resolvable file paths — that is what makes the §6 dual-linking guarantee checkable. The pre-migration `source:` string is *encounter provenance* and belongs in the `## Source` body section instead. Moving it is a relocation, not a conversion, and loses nothing. Do this when you touch a note for another reason; do not bulk-migrate.",
              legacy[:15]))

    # 8 ── overdue assessment
    over = [n for n in comp if n["fm"].get("so_what") == "not yet assessed"]
    over.sort(key=lambda n: -num(n["fm"].get("signal_strength")))
    L.append(("Overdue assessment", f"{len(over)} notes still carry no so-what. Listed strongest first — working down this list is the single highest-value manual task on the vault.",
              [f"**{num(n['fm'].get('signal_strength'))}** · [[{n['name']}]]" for n in over[:15]]))

    # 9 ── attention gap (loop 4)
    unused = [n for n in comp
              if num(n["fm"].get("signal_strength")) >= 6 and "last_used" not in n["fm"]]
    unused.sort(key=lambda n: -num(n["fm"].get("signal_strength")))
    L.append(("Attention gap", "Strength 6+ but never recorded as used. High score means the world is talking about it; it does not mean it changed anything you did. If a signal here has genuinely never been useful, that is worth knowing about the scoring — see [[Attention log]].",
              [f"**{num(n['fm'].get('signal_strength'))}** · [[{n['name']}]]" for n in unused[:15]]))

    # ── write ────────────────────────────────────────────────────────────────
    counts = {name: len(items) for name, _, items in L}
    md = [f"""---
title: "Lint report"
type: report
tags: ["meta", "lint"]
generated: {TODAY}
---

# 🔍 Lint report — {TODAY}

Generated by `lint_wiki.py`. **Nothing here has been changed automatically.** Every item is a judgement call; see [[AGENTS]] §7.

Scanned {len(notes)} notes, {len(comp)} compiled.

| Check | Found |
|---|---|
""" + "\n".join(f"| {k} | {v} |" for k, v in counts.items())]

    for name, blurb, items in L:
        md.append(f"\n---\n\n## {name} — {len(items)}\n\n{blurb}\n")
        md.append("\n".join(f"- {i}" for i in items) if items else "*Nothing found.*")

    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"  ✓ {OUT.name} written")
    for k, v in counts.items():
        print(f"    {k:32} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
