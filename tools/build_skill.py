#!/usr/bin/env python3
"""Build the uploadable skill zip: dist/obsidian-wiki.zip

    python3 tools/build_skill.py

Assembles skill/obsidian-wiki/ plus the starter vault (vault/) and the
weak-signals add-on (addons/weak-signals/) as assets. The vault and add-on are
copied at build time rather than kept twice in the repo, so there is only ever
one source for each file.
"""
import shutil
import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):   # Windows consoles default to a non-UTF-8 code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skill" / "obsidian-wiki"
BUILD = ROOT / "dist" / "build" / "obsidian-wiki"
OUT = ROOT / "dist" / "obsidian-wiki.zip"
SKIP = {"__pycache__", ".DS_Store", "_LINT.md", "signals.json", ".backup_vault.log"}


def copytree(src, dst):
    shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in SKIP or n.endswith(".pyc")])


def main():
    if BUILD.parent.exists():
        shutil.rmtree(BUILD.parent)
    copytree(SKILL, BUILD)
    copytree(ROOT / "vault", BUILD / "assets" / "vault")
    copytree(ROOT / "addons" / "weak-signals", BUILD / "assets" / "addons" / "weak-signals")
    for lic in ("LICENSE", "LICENSE-docs.md"):
        shutil.copy(ROOT / lic, BUILD / lic)

    OUT.parent.mkdir(exist_ok=True)
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(BUILD.rglob("*")):
            if f.is_file():
                # the skill folder must be the zip's root entry
                z.write(f, Path("obsidian-wiki") / f.relative_to(BUILD))
    n = len(zipfile.ZipFile(OUT).namelist())
    print(f"✓ {OUT.relative_to(ROOT)} — {n} files, {OUT.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
