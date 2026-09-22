# Cognitive Agent Literature

A weekly-reviewed, curated literature repository on **cognitive agents**:
how they are framed/presented, how they are programmed, and what is
currently happening in the field.

- **Curator:** `mind` (the cognition agent of the mymate crew)
- **Cadence:** a new edition every week
- **Reminder:** the captain is warned 1 day before each weekly review
- **Review flow:** captain reviews the collected literature, then we
  present the new edition here (commit + push to this repo)

## Structure

```
README.md                      – this file (also acts as the update log)
docs/                          – standalone knowledge pages (self-contained HTML)
  cognitive-agents.html        – v1: cognitive agents knowledge page
  tutorial-cognitive.html      – v2: BDI cognitive architecture tutorial (cognitive.js)
editions/                      – one file per weekly edition
  2026-W38-cognitive-agents.md – seed edition (report on cognitive agents, Sep 2026)
tools/remind-weekly.ps1        – the weekly reminder script (Windows scheduled task)
```

## Knowledge pages

| Version | Page | Date | Notes |
| --- | --- | --- | --- |
| v1 | [docs/cognitive-agents.html](docs/cognitive-agents.html) | 2026-09-18 | Framing, CoALA, BDI, SDKs, standards, evals, safety, cabin sim |
| v2 | [docs/tutorial-cognitive.html](docs/tutorial-cognitive.html) | 2026-09-22 | BDI architecture tutorial for `cognitive.js`: state S/PHILL, ROT/HGT tables, cognition loop, memory decay λ=0.004, trust & mood formulas, event timeline, `__EXPERIMENTER_CHAT__` hook, parameters |

## Weekly update log

| Week | Edition | Date | Notes |
| --- | --- | --- | --- |
| 2026-W38 | [2026-W38-cognitive-agents.md](editions/2026-W38-cognitive-agents.md) | 2026-09-17 | Seed edition: framing, programming practice, current events (source: `mind`) |

## What a weekly run does

1. `mind` looks up fresh literature (research papers, framework releases,
   product/news) using live web search, grounded in real sources.
2. `mind` improves/expands the previous edition + adds a new dated edition
   file, keeping it readable and no longer than ~5 pages per edition.
3. The captain reviews; we present the new version and push it here.

## Reminder

A Windows scheduled task (`CognitiveAgentLiterature-WeeklyReminder`) fires
every Sunday at 09:00 — i.e. 1 day before the Monday weekly refresh — and
shows a desktop toast pointing at this repo.