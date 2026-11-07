#!/usr/bin/env python3
"""Nightly vault backup with git — works on Mac, Windows and Linux.

    python3 backup_vault.py              # back up now (Windows: py backup_vault.py)
    python3 backup_vault.py --install    # run it every night at 21:00
    python3 backup_vault.py --install --time 22:30
    python3 backup_vault.py --remove     # stop the nightly run
    python3 backup_vault.py --status     # is the nightly run set up?

What a backup does: commit every change in the vault, then push if a remote is
set up. If the push fails, it says so loudly — in the log AND as a note at
`Admin/⚠️ Backup problem.md`, which you'll see in Obsidian. A stale backup
looks identical to a working one from outside, so it must never fail quietly.

Why this runs from your computer's own scheduler (launchd / Task Scheduler /
cron) and NOT as a Claude scheduled task: Claude's sandbox can create files
inside .git but sometimes cannot delete them, so a sandboxed `git commit` can
leave a stale lock that blocks your next git command.

NEVER add `git clean` to this script. It deletes untracked files permanently.
"""
import argparse
import datetime as dt
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent
LOG = VAULT / ".backup_vault.log"
ADMIN = VAULT / "Admin" if (VAULT / "Admin").is_dir() else VAULT
PROBLEM = ADMIN / "⚠️ Backup problem.md"
LABEL = "com.obsidian-claude-wiki.vault-backup"   # macOS launchd label
TASK = "Obsidian vault backup"                   # Windows Task Scheduler name
SYSTEM = platform.system()                       # "Darwin" | "Windows" | "Linux"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def log(msg):
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def git(*args, check=False):
    exe = shutil.which("git")
    if not exe:
        log("git not found — install it first (see SETUP.md)")
        sys.exit(1)
    flags = subprocess.CREATE_NO_WINDOW if SYSTEM == "Windows" else 0
    return subprocess.run([exe, *args], cwd=VAULT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=check, creationflags=flags)


def flag_problem(text):
    PROBLEM.write_text(f"""---
title: "Backup problem"
type: meta
---

# ⚠️ Backup problem — {dt.date.today()}

{text}

This note disappears by itself after the next successful backup. Full log: `.backup_vault.log` in the vault folder.
""", encoding="utf-8")


def clear_problem():
    if PROBLEM.exists():
        PROBLEM.unlink()


def backup():
    if not (VAULT / ".git").is_dir():
        log("no git repository here — run `git init` in the vault first (see SETUP.md)")
        return 1

    # A lock left by a dead process blocks every git command. The scheduler runs
    # this one at a time, and a live git holds the lock for seconds, not hours.
    lock = VAULT / ".git" / "index.lock"
    if lock.exists():
        age = dt.datetime.now().timestamp() - lock.stat().st_mtime
        if age > 600:
            lock.unlink()
            log("removed a stale .git/index.lock")

    clear_problem()   # so the problem note itself is never committed
    git("add", "-A")
    if git("diff", "--cached", "--quiet").returncode == 0:
        log("no changes")
        return 0

    files = len(git("diff", "--cached", "--name-only").stdout.splitlines())
    r = git("commit", "-q", "-m", f"Vault backup {dt.date.today()} — {files} files")
    if r.returncode != 0:
        log(f"COMMIT FAILED: {r.stderr.strip() or r.stdout.strip()}")
        flag_problem("The nightly backup could not commit your changes.\n\n"
                     f"```\n{(r.stderr or r.stdout).strip()}\n```\n\n"
                     "If it mentions `user.name` or `user.email`, run the two `git config` commands in SETUP.md step 6.")
        return 1

    if git("remote", "get-url", "origin").returncode != 0:
        log(f"committed {files} files (no remote, not pushed)")
        return 0

    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip() or "main"
    r = git("push", "-q", "origin", branch)
    if r.returncode == 0:
        log(f"committed and pushed {files} files")
        return 0
    log(f"COMMITTED {files} files BUT PUSH FAILED: {r.stderr.strip()}")
    flag_problem("Your changes were saved on this computer, but **could not be copied to GitHub**.\n\n"
                 f"```\n{r.stderr.strip()}\n```\n\n"
                 "Usually expired GitHub credentials. Open a terminal in the vault folder and run `git push` to see the full message.")
    return 1


def crontab_lines():
    """Current crontab lines, or [] if cron isn't available."""
    try:
        return subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout.splitlines()
    except FileNotFoundError:
        return []


# ── scheduling ──────────────────────────────────────────────────────────────

def python_for_scheduler():
    exe = Path(sys.executable)
    if SYSTEM == "Windows":
        # pythonw runs without flashing a console window every night
        w = exe.with_name("pythonw.exe")
        return str(w if w.exists() else exe)
    return str(exe)


def install(hh, mm):
    script = str(Path(__file__).resolve())
    py = python_for_scheduler()
    if SYSTEM == "Darwin":
        plist = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
        plist.parent.mkdir(parents=True, exist_ok=True)
        plist.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>{LABEL}</string>
    <key>ProgramArguments</key>
    <array><string>{py}</string><string>{script}</string></array>
    <key>StartCalendarInterval</key>
    <dict><key>Hour</key><integer>{hh}</integer><key>Minute</key><integer>{mm}</integer></dict>
    <key>StandardErrorPath</key><string>{VAULT / '.backup_vault.err'}</string>
</dict>
</plist>
""", encoding="utf-8")
        subprocess.run(["launchctl", "unload", str(plist)], capture_output=True)
        r = subprocess.run(["launchctl", "load", str(plist)], capture_output=True, text=True)
        ok = r.returncode == 0
    elif SYSTEM == "Windows":
        tr = f'"{py}" "{script}"'
        r = subprocess.run(["schtasks", "/Create", "/F", "/SC", "DAILY", "/TN", TASK,
                            "/TR", tr, "/ST", f"{hh:02d}:{mm:02d}"],
                           capture_output=True, text=True)
        ok = r.returncode == 0
    else:
        line = f'{mm} {hh} * * * "{py}" "{script}"  # {LABEL}'
        keep = [l for l in crontab_lines() if LABEL not in l]
        try:
            r = subprocess.run(["crontab", "-"], input="\n".join(keep + [line]) + "\n",
                               capture_output=True, text=True)
            ok = r.returncode == 0
        except FileNotFoundError:
            print("✗ cron isn't available on this system; schedule `backup_vault.py` another way.")
            return 1
    if ok:
        print(f"✓ Nightly backup set for {hh:02d}:{mm:02d}. Log: {LOG}")
        print("  Your computer must be on (it can be asleep on a Mac) at that time.")
        return 0
    print(f"✗ Could not set up the nightly backup:\n{r.stderr or r.stdout}")
    return 1


def remove():
    if SYSTEM == "Darwin":
        plist = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
        subprocess.run(["launchctl", "unload", str(plist)], capture_output=True)
        if plist.exists():
            plist.unlink()
    elif SYSTEM == "Windows":
        subprocess.run(["schtasks", "/Delete", "/F", "/TN", TASK], capture_output=True)
    else:
        keep = [l for l in crontab_lines() if LABEL not in l]
        try:
            subprocess.run(["crontab", "-"], input="\n".join(keep) + "\n", text=True)
        except FileNotFoundError:
            pass
    print("✓ Nightly backup removed.")
    return 0


def status():
    if SYSTEM == "Darwin":
        on = (Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist").exists()
    elif SYSTEM == "Windows":
        on = subprocess.run(["schtasks", "/Query", "/TN", TASK], capture_output=True).returncode == 0
    else:
        on = any(LABEL in l for l in crontab_lines())
    print("✓ Nightly backup is set up." if on else "✗ Nightly backup is not set up. Run with --install.")
    if LOG.exists():
        last = LOG.read_text(encoding="utf-8").strip().splitlines()[-1:]
        if last:
            print(f"  Last run: {last[0]}")
    return 0 if on else 1


def main():
    ap = argparse.ArgumentParser(description="Back up the vault with git.")
    ap.add_argument("--install", action="store_true", help="run nightly")
    ap.add_argument("--remove", action="store_true", help="stop the nightly run")
    ap.add_argument("--status", action="store_true", help="show whether the nightly run is set up")
    ap.add_argument("--time", default="21:00", help="HH:MM for --install (default 21:00)")
    a = ap.parse_args()
    if a.install:
        hh, mm = (int(x) for x in a.time.split(":"))
        return install(hh, mm)
    if a.remove:
        return remove()
    if a.status:
        return status()
    return backup()


if __name__ == "__main__":
    sys.exit(main())
