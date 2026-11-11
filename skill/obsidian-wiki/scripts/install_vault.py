#!/usr/bin/env python3
"""Build or update an Obsidian wiki vault from this skill's assets.

    python3 install_vault.py --target <vault folder> --answers answers.json
    python3 install_vault.py --target <vault folder> --update

New install: copies the starter vault, fills in AGENTS.md §0 from the answers,
writes Admin/wiki-settings.md, renames or removes the extra category, installs
and configures the Dataview and Git Obsidian plugins, and (optionally) the
weak-signals add-on. It never overwrites an existing file.

Update: refreshes scripts, Admin/prompts/ and Admin/_templates/, and writes the
new rulebook to Admin/AGENTS.new.md for merging. Never touches notes or settings.

Never deletes anything. Prints a JSON summary; exit code 0 on success.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent.parent          # the skill folder
ASSETS = HERE / "assets"
VAULT_SRC = ASSETS / "vault"
ADDON_SRC = ASSETS / "addons" / "weak-signals"
OBS_SRC = ASSETS / "obsidian"
DEFAULT_EXTRA = "Energy"
BAD = set(':?*"<>|/\\')
IGNORABLE = {".DS_Store", "Thumbs.db", "desktop.ini", ".localized"}

created, skipped, notes = [], [], []


def fail(msg):
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False, indent=2))
    sys.exit(1)


def write_new(dst: Path, data, binary=False):
    """Write a file only if it doesn't exist yet."""
    if dst.exists():
        skipped.append(str(dst))
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if binary:
        dst.write_bytes(data)
    else:
        dst.write_text(data, encoding="utf-8", newline="\n")
    created.append(str(dst))
    return True


def overwrite(dst: Path, data, binary=False):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if binary:
        dst.write_bytes(data)
    else:
        dst.write_text(data, encoding="utf-8", newline="\n")
    created.append(str(dst))


def is_text(p: Path):
    return p.suffix.lower() in {".md", ".py", ".json", ".txt", ".css", ".yml", ".gitignore"} or p.name == ".gitignore"


# ── new install ──────────────────────────────────────────────────────────────

def category_transform(extra):
    """Return a function mapping (relative path, text) → (relative path, text) or None to skip."""
    def tf(rel: str, text):
        if extra == DEFAULT_EXTRA:
            return rel, text
        if extra is None:
            if rel == "10 Notes/+Energy.md" or rel == "10 Notes/Energy/.gitkeep":
                return None
            if rel.startswith("10 Notes/Energy/"):
                rel = rel.replace("10 Notes/Energy/", "10 Notes/Environmental/", 1)
                if text is not None:
                    text = text.replace("pestle: Energy", "pestle: Environmental")
            if text is not None and rel == "+Home.md":
                text = "\n".join(l for l in text.split("\n") if "[[+Energy]]" not in l)
            return rel, text
        rel = rel.replace("10 Notes/Energy/", f"10 Notes/{extra}/", 1).replace("10 Notes/+Energy.md", f"10 Notes/+{extra}.md", 1)
        if text is not None:
            if rel == f"10 Notes/+{extra}.md":
                text = text.replace("Energy", extra).replace("Your extra category — rename to suit your focus", f"Your own category: {extra}")
            text = text.replace("pestle: Energy", f"pestle: {extra}")
            if rel == "+Home.md":
                text = text.replace("[[+Energy]] | Your extra category — rename to suit your focus", f"[[+{extra}]] | Your own category")
        return rel, text
    return tf


def fill_agents(text, a, extra):
    owner = a.get("owner") or "TODO (your name)"
    focus = a.get("focus") or "TODO"
    so_what = a.get("so_what") or (f"What does this mean for {focus}?" if a.get("focus") else None)
    cats = ["Economic"] + ([extra] if extra else []) + ["Environmental", "Legal", "Political", "Social", "Technological"]
    cats_line = ", ".join(f"`{c}`" for c in cats)
    repl = [
        (r"^- \*\*Owner:\*\* .*$", f"- **Owner:** {owner}"),
        (r"^- \*\*Focus / lens:\*\* .*$", f"- **Focus / lens:** {focus}"),
        (r"^- \*\*Categories:\*\* .*$",
         f"- **Categories:** {cats_line} — PESTLE" + (f" plus `{extra}`." if extra else ".") +
         " Keep folder names and the `pestle:` field in step."),
    ]
    if so_what:
        repl.append((r'^- \*\*The "so what" question:\*\* .*$', f'- **The "so what" question:** *{so_what}*'))
    for pat, new in repl:
        text, n = re.subn(pat, lambda m: new, text, count=1, flags=re.M)
        if n != 1:
            fail(f"AGENTS.md §0 line not found: {pat}")
    return text


def settings_md(a, target):
    def yl(v):
        return "[" + ", ".join(json.dumps(x, ensure_ascii=False) for x in (v or [])) + "]"
    f = a.get("features") or {}
    return f"""---
title: "Wiki settings"
type: meta
owner: {json.dumps(a.get("owner") or "", ensure_ascii=False)}
vault_path: {json.dumps(a.get("vault_path") or str(target), ensure_ascii=False)}
email: {json.dumps(a.get("email") or "", ensure_ascii=False)}
newsletters: {yl(a.get("newsletters"))}
briefing_topics: {yl(a.get("briefing_topics"))}
timezone: {json.dumps(a.get("timezone") or "", ensure_ascii=False)}
newsletter_sync: {str(bool(f.get("newsletter_sync"))).lower()}
daily_briefing: {str(bool(f.get("daily_briefing"))).lower()}
daily_inspiration: {str(bool(f.get("daily_inspiration"))).lower()}
weak_signals: {str(bool(f.get("weak_signals"))).lower()}
---

# Wiki settings

The scheduled routines read this page for your email, newsletters and topics. Edit it freely — changes apply from the next run.

- **email** — where daily inspiration and the "Your three" heads-up are sent.
- **newsletters** — sender addresses that newsletter sync copies into `00 Inbox/`.
- **briefing_topics** — what the daily briefing searches for.

Your focus and categories live in [[AGENTS]] §0.
"""


def install_obsidian(target: Path):
    obs = target / ".obsidian"
    for plugin in ("dataview", "obsidian-git"):
        src = OBS_SRC / "plugins" / plugin
        for f in src.iterdir():
            write_new(obs / "plugins" / plugin / f.name, f.read_bytes(), binary=True)
    write_new(obs / "community-plugins.json", json.dumps(["dataview", "obsidian-git"], indent=2))
    write_new(obs / "plugins" / "dataview" / "data.json", json.dumps({"enableDataviewJs": True, "renderNullAs": "\\-"}, indent=2))
    write_new(obs / "plugins" / "obsidian-git" / "data.json", json.dumps({
        "autoSaveInterval": 60,                 # snapshot every hour while Obsidian is open
        "autoCommitMessage": "Vault backup: {{date}}",
        "commitMessage": "Vault backup: {{date}}",
        "disablePush": True,                    # switch off once a private remote is added
        "autoPullOnBoot": False,
        "showErrorNotices": True,
        "disablePopupsForNoChanges": True,
    }, indent=2))
    write_new(obs / "templates.json", json.dumps({"folder": "Admin/_templates"}, indent=2))


def new_install(target: Path, a: dict):
    if (target / "Admin" / "AGENTS.md").exists():
        fail("This folder already has a wiki (Admin/AGENTS.md exists). Use --update instead.")
    others = [p.name for p in target.iterdir() if p.name not in IGNORABLE]
    if others and not a.get("allow_non_empty"):
        fail(f"The folder isn't empty ({', '.join(others[:5])}). Choose an empty folder, or set \"allow_non_empty\": true in the answers.")

    extra = a.get("extra_category", DEFAULT_EXTRA)
    if extra is not None:
        extra = str(extra).strip().title() or None
    if extra and (BAD & set(extra) or extra in {"Economic", "Environmental", "Legal", "Political", "Social", "Technological"}):
        fail(f"'{extra}' can't be used as the extra category name.")
    tf = category_transform(extra)

    for src in sorted(VAULT_SRC.rglob("*")):
        if src.is_dir() or "__pycache__" in src.parts:
            continue
        rel = src.relative_to(VAULT_SRC).as_posix()
        text = src.read_text(encoding="utf-8") if is_text(src) else None
        out = tf(rel, text)
        if out is None:
            continue
        rel, text = out
        if rel == "Admin/AGENTS.md":
            text = fill_agents(text, a, extra)
        if rel == "Admin/wiki-settings.md":
            text = settings_md(a, target)
        dst = target / rel
        if text is None:
            write_new(dst, src.read_bytes(), binary=True)
        else:
            write_new(dst, text)
    if extra:
        (target / "10 Notes" / extra).mkdir(parents=True, exist_ok=True)

    install_obsidian(target)

    if (a.get("features") or {}).get("weak_signals"):
        for src in sorted((ADDON_SRC / "60 Signals").rglob("*")):
            if src.is_file():
                write_new(target / "60 Signals" / src.relative_to(ADDON_SRC / "60 Signals"), src.read_text(encoding="utf-8"))
        write_new(target / "build_signals_json.py", (ADDON_SRC / "build_signals_json.py").read_text(encoding="utf-8"))
        write_new(target / "Admin" / "prompts" / "weekly-weak-signals.md", (ADDON_SRC / "weekly-weak-signals.md").read_text(encoding="utf-8"))
        notes.append("weak-signals add-on installed")

    long_paths = [p for p in created if len(p) > 240]
    if long_paths:
        notes.append("Some paths are over 240 characters — Windows may struggle. Consider a shorter vault location.")
    return {"mode": "install", "extra_category": extra}


# ── update ───────────────────────────────────────────────────────────────────

def update(target: Path):
    if not (target / "Admin" / "AGENTS.md").exists():
        fail("No wiki here (Admin/AGENTS.md not found). Use --answers for a new install.")
    for src in VAULT_SRC.glob("*.py"):
        overwrite(target / src.name, src.read_text(encoding="utf-8"))
    for sub in ("prompts", "_templates"):
        for src in (VAULT_SRC / "Admin" / sub).rglob("*"):
            if src.is_file():
                overwrite(target / "Admin" / sub / src.relative_to(VAULT_SRC / "Admin" / sub), src.read_text(encoding="utf-8"))
    if (target / "60 Signals").is_dir():
        overwrite(target / "build_signals_json.py", (ADDON_SRC / "build_signals_json.py").read_text(encoding="utf-8"))
        overwrite(target / "Admin" / "prompts" / "weekly-weak-signals.md", (ADDON_SRC / "weekly-weak-signals.md").read_text(encoding="utf-8"))
        overwrite(target / "60 Signals" / "SIGNALS.md", (ADDON_SRC / "60 Signals" / "SIGNALS.md").read_text(encoding="utf-8"))
    overwrite(target / "Admin" / "AGENTS.new.md", (VAULT_SRC / "Admin" / "AGENTS.md").read_text(encoding="utf-8"))
    write_new(target / "Admin" / "wiki-settings.md", settings_md({}, target))   # only if missing
    notes.append("Merge Admin/AGENTS.new.md into Admin/AGENTS.md, keeping §0 and §8 (see references/update.md).")
    return {"mode": "update"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--answers")
    ap.add_argument("--update", action="store_true")
    a = ap.parse_args()

    target = Path(a.target).expanduser().resolve()
    if not target.is_dir():
        fail(f"Folder not found: {target}")
    if not VAULT_SRC.is_dir():
        fail(f"Skill assets missing: {VAULT_SRC}")

    if a.update:
        info = update(target)
    else:
        if not a.answers:
            fail("--answers is required for a new install")
        answers = json.loads(Path(a.answers).read_text(encoding="utf-8"))
        info = new_install(target, answers)

    print(json.dumps({"ok": True, **info, "target": str(target),
                      "files_written": len(created), "files_skipped_existing": len(skipped),
                      "notes": notes}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
