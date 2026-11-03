# Add-on: weak-signals register

The core vault tells you **how strong each idea is**. This add-on tells you **what the big picture is and how it's moving**: 25–35 signals, each a synthesis across several notes, grouped into themes that an agent challenges every week.

Install it once the core vault has been running for a few weeks. With fewer than ~50 compiled notes there isn't enough to synthesise, and you'll get signals that just restate single notes.

## What you get

- `60 Signals/SIGNALS.md` — the rules for the register (the add-on's equivalent of `AGENTS.md`).
- `60 Signals/+Signals.md` and `Themes/+Themes.md` — Dataview index pages.
- One example signal and one example theme, built from the example notes in the starter vault.
- `build_signals_json.py` — builds `signals.json`, a machine-readable feed with computed `trend` and `momentum`, for any dashboard or app you want to point at it.
- `prompts/weekly-weak-signals.md` — the scheduled task prompt.

## Install

1. Copy the `60 Signals` folder into your vault root.
2. Copy `build_signals_json.py` into your vault root.
3. Check it runs: in Terminal, `cd` to your vault and run `python3 build_signals_json.py`. You should see `✓ signals.json — 1 signals`.
4. Create a weekly scheduled task from `prompts/weekly-weak-signals.md`.
5. After two or three runs, delete the example signal and theme.

`AGENTS.md` already reserves `60 Signals/` for this agent, so no changes are needed there.

## The three ideas that make it work

- **A signal is not a note.** If a signal restates one note, it isn't a signal. The value is in what gets left out — about one signal per ten notes.
- **Themes group by mechanism, not topic.** Left alone, themes turn into topic buckets. The weekly run tests membership by asking which dynamic each signal shows.
- **Every theme needs a tension.** The counter-force that might make the theme wrong. A theme without one is just a category.

## `signals.json`

Treat it as private: summaries usually contain commentary about your own organisation. Each signal has `id`, `title`, `trend` (`rising` / `steady` / `declining`), `strength`, `momentum` (−1 to 1), `maturity`, `impact`, `theme`, `first_seen`, `last_updated`, `summary`, `tags` and up to six `sources`. `maturity` and `impact` are laid out as x and y axes, so it plots directly as a bubble chart.
