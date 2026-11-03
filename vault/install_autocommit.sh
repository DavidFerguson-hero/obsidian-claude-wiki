#!/bin/bash
# Installs a macOS launchd job that runs commit_vault.sh every night at 21:00.
#
#   ./install_autocommit.sh            # install (or reinstall)
#   ./install_autocommit.sh --remove   # uninstall
#
# Pick a time AFTER your Claude scheduled tasks have run, so each day's agent
# changes land in one reviewable commit.

set -eu
VAULT="$(cd "$(dirname "$0")" && pwd)"
LABEL="com.obsidian-claude-wiki.vault-commit"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
HOUR="${HOUR:-21}"
MINUTE="${MINUTE:-0}"

if [ "${1:-}" = "--remove" ]; then
    launchctl unload "$PLIST" 2>/dev/null || true
    rm -f "$PLIST"
    echo "Removed $PLIST"
    exit 0
fi

if [ ! -d "$VAULT/.git" ]; then
    echo "No git repository in $VAULT — run 'git init' there first (see SETUP.md)."
    exit 1
fi

chmod +x "$VAULT/commit_vault.sh"
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$VAULT/commit_vault.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>$HOUR</integer>
        <key>Minute</key>
        <integer>$MINUTE</integer>
    </dict>
    <key>StandardErrorPath</key>
    <string>$VAULT/.commit_vault.err</string>
</dict>
</plist>
EOF

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "Installed: vault will autocommit daily at $(printf '%02d:%02d' "$HOUR" "$MINUTE")."
echo "Log: $VAULT/.commit_vault.log"
