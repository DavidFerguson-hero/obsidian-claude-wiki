# Update an existing wiki

Use when the user has uploaded a newer version of this skill and says "update my wiki".

1. **Find the vault** (the connected folder with `Admin/AGENTS.md`).
2. **Run the installer in update mode** (see "Running the bundled scripts" in `SKILL.md`):

   ```
   python3 scripts/install_vault.py --target "<vault folder>" --update
   ```

   This refreshes the scripts, `Admin/prompts/` and `Admin/_templates/`, and writes the new rulebook to `Admin/AGENTS.new.md`. It **never** touches notes, the inbox, the archive, signals, `Admin/AGENTS.md`, `Admin/wiki-settings.md` or the attention log.

3. **Merge the rulebook.** Compare `Admin/AGENTS.new.md` with `Admin/AGENTS.md`:
   - Keep the user's **§0** and **§8** exactly as they are.
   - Bring in every other change from the new version.
   - Show the user a short list of what changed (one line each), and ask before writing.
   - On a yes, write the merged result to `Admin/AGENTS.md`. Leave `AGENTS.new.md` for the user to delete.
4. **Check:** from the vault folder, run `python3 check_setup.py --agent`, and report anything to fix.
5. **Scheduled tasks** don't need changing — their one-line prompts call this skill, so they pick up the new version automatically.
