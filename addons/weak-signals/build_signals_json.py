#!/usr/bin/env python3
"""
Build signals.json — the weak-signals feed
==========================================
Reads `60 Signals/`, writes `signals.json` to the vault root — a machine-readable
feed any dashboard or app can read.

Treat it as private by default: signal summaries usually carry commentary about
your own organisation. There is deliberately no publish step in this file.

This script makes no judgements. `trend` and `momentum` are computed from the
dated evidence in each signal's member notes; everything else is read from the
signal notes, which the weak-signals agent maintains.

    python3 build_signals_json.py
    python3 build_signals_json.py --stdout   # print, don't write
"""

import json, re, sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT    = Path(__file__).parent
SIGNALS = ROOT / "60 Signals"
NOTES   = ROOT / "10 Notes"
OUT     = ROOT / "signals.json"

TREND_ENUM    = {"rising", "steady", "declining"}
STRENGTH_ENUM = {"weak", "emerging", "established", "strong"}

# momentum window: evidence in the last N days vs the N days before that
WINDOW = 45


def parse_fm(text):
    m = re.match(r"^---\n(.*?)\n---", text, flags=re.S)
    if not m:
        return None, text
    fm, cur = {}, None
    for line in m.group(1).split("\n"):
        li = re.match(r"^\s*-\s*(.*)$", line)
        if li and cur:
            fm[cur].append(li.group(1).strip().strip('"'))
            continue
        km = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if not km:
            continue
        k, v = km.group(1), km.group(2).strip()
        if v == "":
            fm[k] = []; cur = k; continue
        cur = None
        if v.startswith('"') and v.endswith('"') and len(v) > 1:
            v = v[1:-1]
        elif v.startswith("[") and v.endswith("]"):
            try: v = json.loads(v)
            except Exception: pass
        fm[k] = v
    return fm, text[m.end():]


def num(v, d=None):
    try: return float(v)
    except (TypeError, ValueError): return d


def note_index():
    idx = {}
    if NOTES.exists():
        for p in NOTES.rglob("*.md"):
            idx[p.stem] = p
    return idx


def evidence_dates(names, idx):
    """Every dated evidence entry across a signal's member notes.

    Excludes any `### Curated signal …` blocks. If you migrate signals in from an
    older system, put them under that heading: they carry the date of the
    migration, not the date anything happened, and counting them would make the
    feed measure its own housekeeping.
    """
    out = []
    for n in names:
        p = idx.get(str(n).strip("[]"))
        if not p:
            continue
        try: t = p.read_text(encoding="utf-8")
        except OSError: continue
        blk = re.search(r"^##\s*Supporting evidence\s*$(.*?)(?=^##\s|\Z)", t, flags=re.S | re.M)
        text = blk.group(1) if blk else t
        # drop migration blocks: from the ### heading to the next ## / ### or end
        text = re.sub(r"^###\s*Curated signal.*?(?=^#{2,3}\s|\Z)", "", text, flags=re.S | re.M)
        for d in re.findall(r"\*\((20\d\d-\d\d-\d\d)\)\*", text):
            try: out.append(datetime.strptime(d, "%Y-%m-%d").date())
            except ValueError: pass
    return sorted(out)


MIN_SAMPLE = 3   # below this, a direction is noise dressed up as a finding


def momentum_and_trend(dates):
    """Accretion rate: recent evidence vs the preceding window. -1..1.

    Guarded by sample size. One evidence entry in the recent window and none before
    gives a raw ratio of 1.0 — mathematically maximal, evidentially meaningless. With
    fewer than MIN_SAMPLE entries across both windows we report `steady` and a damped
    momentum, because a single data point is not a direction.
    """
    if not dates:
        return 0.0, "steady"
    today = date.today()
    recent = sum(1 for d in dates if (today - d).days <= WINDOW)
    prior  = sum(1 for d in dates if WINDOW < (today - d).days <= WINDOW * 2)
    n = recent + prior
    if n == 0:
        return 0.0, "steady"
    mom = (recent - prior) / n
    if n < MIN_SAMPLE:
        # keep the sign as a hint, but damp it and refuse to call a trend
        return round(mom * (n / MIN_SAMPLE), 2), "steady"
    mom = round(max(-1.0, min(1.0, mom)), 2)
    trend = "rising" if mom >= 0.25 else "declining" if mom <= -0.25 else "steady"
    return mom, trend


def sources_from(names, idx, cap=6):
    """{title,url} pairs harvested from the member notes' evidence links."""
    seen, out = set(), []
    for n in names:
        p = idx.get(str(n).strip("[]"))
        if not p:
            continue
        try: t = p.read_text(encoding="utf-8")
        except OSError: continue
        blk = re.search(r"^##\s*Supporting evidence\s*$(.*?)(?=^##\s|\Z)", t, flags=re.S | re.M)
        for mt, url in re.findall(r"\[([^\]]{8,140})\]\((https?://[^\s)]+)\)", blk.group(1) if blk else ""):
            if url in seen:
                continue
            seen.add(url)
            out.append({"title": re.sub(r"\s+", " ", mt).strip()[:140], "url": url})
            if len(out) >= cap:
                return out
    return out


def main():
    if not SIGNALS.exists():
        print(f"✗ {SIGNALS} not found — install the weak-signals add-on first"); return 1

    idx = note_index()
    signals, problems = [], []

    for p in sorted(SIGNALS.rglob("*.md")):
        fm, _ = parse_fm(p.read_text(encoding="utf-8"))
        if not fm or fm.get("type") != "signal":
            continue
        if fm.get("status") == "retired":
            continue

        members = fm.get("evidence_notes") or []
        if isinstance(members, str):
            members = [members]
        members = [re.sub(r"^\[\[|\]\]$", "", m) for m in members]

        dates = evidence_dates(members, idx)
        mom, trend = momentum_and_trend(dates)

        sig = {
            "id":      fm.get("signal_id") or p.stem,
            "title":   fm.get("title") or p.stem,
            "trend":   trend,
            "strength": fm.get("strength", "emerging"),
        }
        if fm.get("summary_text"): sig["summary"] = fm["summary_text"]
        if fm.get("theme"):        sig["theme"]   = fm["theme"]
        for k, src in (("maturity", "maturity"), ("impact", "impact")):
            v = num(fm.get(src))
            if v is not None: sig[k] = v
        sig["momentum"] = mom
        fs = fm.get("first_seen")
        if fs and fs != "unknown":
            sig["first_seen"] = fs
        elif dates:
            sig["first_seen"] = dates[0].isoformat()
        sig["last_updated"] = (dates[-1].isoformat() + "T00:00:00Z") if dates else \
                              datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        src = sources_from(members, idx)
        if src: sig["sources"] = src
        tags = fm.get("tags")
        if isinstance(tags, list) and tags: sig["tags"] = [t for t in tags if t != "signal"]

        # summary from the note body if not in frontmatter
        if "summary" not in sig:
            body = p.read_text(encoding="utf-8")
            sm = re.search(r"^##\s*Summary\s*$\n(.*?)(?=\n##\s|\Z)", body, flags=re.S | re.M)
            if sm:
                sig["summary"] = re.sub(r"\s+", " ", sm.group(1)).strip()[:400]

        if sig["trend"] not in TREND_ENUM:      problems.append(f"{p.name}: bad trend {sig['trend']}")
        if sig["strength"] not in STRENGTH_ENUM: problems.append(f"{p.name}: bad strength {sig['strength']}")
        signals.append(sig)

    signals.sort(key=lambda s: (-s.get("momentum", 0), -s.get("impact", 0)))

    feed = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "obsidian-weak-signals",
        "axes": {
            "x": {"label": "Maturity", "min": 0, "max": 10},
            "y": {"label": "Potential impact", "min": 0, "max": 10},
        },
        "signals": signals,
    }
    text = json.dumps(feed, ensure_ascii=False, indent=2)

    if "--stdout" in sys.argv:
        print(text); return 0

    OUT.write_text(text, encoding="utf-8")

    import collections
    print(f"  ✓ {OUT.name} — {len(signals)} signals, {len(text):,} bytes")
    print(f"    trend:    {dict(collections.Counter(s['trend'] for s in signals))}")
    print(f"    strength: {dict(collections.Counter(s['strength'] for s in signals))}")
    print(f"    themes:   {len({s.get('theme') for s in signals if s.get('theme')})}")
    print(f"    with sources: {sum(1 for s in signals if s.get('sources'))}")
    if problems:
        print(f"\n  ⚠️  {len(problems)} contract violations:")
        for x in problems: print(f"    {x}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
