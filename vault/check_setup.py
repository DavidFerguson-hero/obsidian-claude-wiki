#!/usr/bin/env python3
"""Checks your vault is set up correctly and says what to fix, in plain words.

    python3 check_setup.py           (Windows: py check_setup.py)
    python3 check_setup.py --agent   when Claude runs it for you (skips checks of
                                     your computer's own Python, git and scheduler,
                                     which Claude's shell can't see)

Reads only. Changes nothing.
"""
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VAULT = Path(__file__).resolve().parent
AGENT = "--agent" in sys.argv
SYSTEM = platform.system()
PY = "py" if SYSTEM == "Windows" else "python3"
BAD_CHARS = set(':?*"<>|')       # not allowed in Windows file names
results = []                     # (ok, message, fix)


def check(ok, msg, fix=""):
    results.append((ok, msg, fix))


# ── tools ────────────────────────────────────────────────────────────────────
if not AGENT:
  check(sys.version_info >= (3, 9), f"Python {platform.python_version()}",
      "Install Python 3.9 or newer from https://www.python.org/downloads/")
git = None if AGENT else shutil.which("git")
if not AGENT:
  check(bool(git), "git installed" if git else "git not found",
      "Mac: run `xcode-select --install`. Windows: install from https://git-scm.com/download/win")

# ── folders ──────────────────────────────────────────────────────────────────
for d in ["00 Inbox", "10 Notes", "Admin", "Admin/_templates", "40 Archive/Processed captures"]:
    check((VAULT / d).is_dir(), f"folder `{d}/`", f"Create the folder `{d}` inside your vault.")

agents = VAULT / "Admin" / "AGENTS.md"
if agents.exists():
    sec0 = agents.read_text(encoding="utf-8").split("## 1.")[0]
    fields = [l for l in sec0.splitlines() if l.startswith("- **")]   # the bullet lines, not the instructions above them
    check(bool(fields) and not any("TODO" in l for l in fields), "AGENTS.md §0 filled in",
          "Open Admin/AGENTS.md and replace each TODO in section 0 with your name and focus.")
else:
    check(False, "Admin/AGENTS.md exists", "Copy AGENTS.md from the starter kit into Admin/.")

# ── Obsidian + Dataview ──────────────────────────────────────────────────────
obs = VAULT / ".obsidian"
if not obs.is_dir():
    check(False, "opened in Obsidian", "Open this folder in Obsidian: 'Open folder as vault'.")
else:
    try:
        plugins = json.loads((obs / "community-plugins.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        plugins = []
    check("dataview" in plugins, "Dataview plugin enabled",
          "Obsidian → Settings → Community plugins → Browse → install and enable Dataview.")
    if (VAULT / "60 Signals").is_dir():
        try:
            dv = json.loads((obs / "plugins" / "dataview" / "data.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            dv = {}
        check(dv.get("enableDataviewJs") is True, "Dataview JavaScript queries on (needed for the signals map)",
              "Obsidian → Settings → Dataview → switch on 'Enable JavaScript queries'.")

# ── git + backup ─────────────────────────────────────────────────────────────
if AGENT:
    gitp = obs / "plugins" / "obsidian-git" / "main.js"
    if gitp.exists():
        check((VAULT / ".git").is_dir(), "backups set up (Git plugin + repository)",
              "In Obsidian press Ctrl/Cmd+P, run 'Git: Initialize a new repo', then 'Git: Commit all changes'. Needs git installed on the computer.")
    else:
        check((VAULT / ".git").is_dir(), "vault is a git repository", "Set up backups — see SETUP.md step 8.")
elif git:
    is_repo = (VAULT / ".git").is_dir()
    check(is_repo, "vault is a git repository", "In a terminal in the vault folder: `git init` (SETUP.md step 6).")
    if is_repo:
        name = subprocess.run([git, "config", "user.name"], cwd=VAULT, capture_output=True, text=True).stdout.strip()
        check(bool(name), "git knows your name", 'Run: git config --global user.name "Your Name"  and  git config --global user.email "you@example.com"')
        sched = subprocess.run([sys.executable, str(VAULT / "backup_vault.py"), "--status"],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
        check(sched.returncode == 0, "nightly backup scheduled", f"Run: {PY} backup_vault.py --install")

# ── location ─────────────────────────────────────────────────────────────────
p = str(VAULT).lower()
synced = next((s for s in ("onedrive", "icloud", "mobile documents", "dropbox", "google drive") if s in p), None)
check(not synced, "vault is outside cloud-sync folders" if not synced else f"vault is inside {synced}",
      "Move the vault out of OneDrive / iCloud / Dropbox (e.g. to C:\\Vaults or ~/Obsidian). Sync services and git conflict, and cloud-only files can be invisible to Claude.")

longest = max((len(str(f)) for f in VAULT.rglob("*") if ".git" not in f.parts), default=0)
if not AGENT:   # Claude sees the vault through a different path, so its length means nothing here
  check(longest < 240, f"longest file path {longest} characters",
      "Windows struggles with paths over 260 characters. Move the vault somewhere shorter, e.g. C:\\Vaults\\Wiki.")

bad = [f.name for f in VAULT.rglob("*.md") if ".git" not in f.parts and BAD_CHARS & set(f.name)]
check(not bad, "note names are Windows-safe" if not bad else f"{len(bad)} note names use : ? * \" < > |",
      "Rename these so the vault opens on Windows too: " + ", ".join(bad[:5]))

# ── report ───────────────────────────────────────────────────────────────────
print(f"\nChecking {VAULT}\n")
for ok, msg, fix in results:
    print(f"  {'✓' if ok else '✗'} {msg}")
    if not ok and fix:
        print(f"      → {fix}")
fails = sum(1 for ok, _, _ in results if not ok)
print("\nAll good." if not fails else f"\n{fails} thing{'s' if fails > 1 else ''} to fix.")
sys.exit(1 if fails else 0)
