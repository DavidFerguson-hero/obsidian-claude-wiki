#!/bin/bash
# Nightly vault autocommit — your safety net against an agent making a mess.
#
# Run nightly by launchd (macOS). Install with:  ./install_autocommit.sh
# Safe to run by hand at any time:             ./commit_vault.sh
#
# Why this is a launchd job and NOT a Claude scheduled task: Claude's sandbox
# can create files inside .git but sometimes cannot delete them, so a sandboxed
# `git commit` can leave a stale index.lock that blocks your next git command.

set -u
VAULT="$(cd "$(dirname "$0")" && pwd)"
GIT="$(command -v git || echo /usr/bin/git)"
LOG="$VAULT/.commit_vault.log"

cd "$VAULT" || { echo "$(date '+%F %T') vault not found" >> "$LOG"; exit 1; }

# Clear a stale lock left by a dead process. launchd runs this serially, and a
# genuine concurrent git would hold the lock for seconds, not hours.
[ -f .git/index.lock ] && rm -f .git/index.lock

$GIT add -A

# Nothing staged means nothing changed today. Exit quietly rather than
# creating empty commits.
if $GIT diff --cached --quiet; then
    echo "$(date '+%F %T') no changes" >> "$LOG"
    exit 0
fi

FILES=$($GIT diff --cached --name-only | wc -l | tr -d ' ')
$GIT commit -q -m "Vault autocommit $(date '+%Y-%m-%d') — $FILES files" >> "$LOG" 2>&1

# No remote configured? A local history is still a full safety net.
if ! $GIT remote get-url origin >/dev/null 2>&1; then
    echo "$(date '+%F %T') committed $FILES files (no remote, not pushed)" >> "$LOG"
    exit 0
fi

BRANCH=$($GIT rev-parse --abbrev-ref HEAD)
if $GIT push -q origin "$BRANCH" >> "$LOG" 2>&1; then
    echo "$(date '+%F %T') committed and pushed $FILES files" >> "$LOG"
else
    # Say so loudly: a stale backup looks identical to a working one from outside.
    echo "$(date '+%F %T') COMMITTED $FILES files BUT PUSH FAILED — check credentials" >> "$LOG"
    osascript -e 'display notification "Vault committed locally but push failed" with title "Obsidian backup"' 2>/dev/null
fi
