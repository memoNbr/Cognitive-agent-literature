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
README.md                      -- this file (also acts as the update log)
docs/                          -- standalone knowledge pages (self-contained HTML)
  cognitive-agents.html        -- v1: cognitive agents knowledge page
  tutorial-cognitive.html      -- v2: BDI cognitive architecture tutorial (cognitive.js)
  tutorial-cognitive-v2.html   -- v2 (Python): BDI cognitive architecture tutorial (cabin_sim/cognition.py, Python-authoritative)
  tutorial-cognitive-v3.html   -- v3: CoALA vs our cabin agent - side-by-side mapping with overlap/diverge/absent verdicts, our code walkthrough, terminology, and what is ours rather than the literature's
  coala-vs-ours-diagram.html    -- schematic: CoALA and ours as a whiteboard, side by side, with the
                                  verdict per row, the beat cycle with the missing learning arrow,
                                  the classic-blackboard lineage, and Mermaid source
  backend-architecture.html      -- whiteboard map of the whole cabin-agent-sim backend: what the
                                  captain authors on disk, the Python process, the browser, one beat
                                  end to end, the chat path, and what is currently wrong
editions/                      -- one file per weekly edition
  2026-W38-cognitive-agents.md -- seed edition (report on cognitive agents, Sep 2026)
tools/remind-weekly.ps1        -- the weekly reminder script (Windows scheduled task)
```

## Knowledge pages

| Version | Page | Date | Notes |
| --- | --- | --- | --- |
| v1 | [docs/cognitive-agents.html](docs/cognitive-agents.html) | 2026-09-18 | Framing, CoALA, BDI, SDKs, standards, evals, safety, cabin sim |
| v2 (JS) | [docs/tutorial-cognitive.html](docs/tutorial-cognitive.html) | 2026-09-22 | BDI architecture tutorial for `cognitive.js`: state S/PHILL, ROT/HGT tables, cognition loop, memory decay =0.004, trust & mood formulas, event timeline, `__EXPERIMENTER_CHAT__` hook, parameters |
| v2 (Py) | [docs/tutorial-cognitive-v2.html](docs/tutorial-cognitive-v2.html) | 2026-09-24 | Python-authoritative BDI tutorial for `cabin_sim/cognition.py`: Mind class, step loop, memory, trust & mood, ride script, schema snapshot, experimenter chat, determinism, reasoning modes (Groq/Ollama/rules), parameters |
| v3 | [docs/tutorial-cognitive-v3.html](docs/tutorial-cognitive-v3.html) | 2026-09-28 | CoALA vs the cabin agent: the four memory systems mapped to ours with an explicit verdict per component (4 overlap, 1 diverges, 2 simplified, 1 absent), the real code for one decision beat, retrieval scoring where we contradict Generative Agents, a terminology table, and the three points that are ours rather than the literature's. Supersedes the earlier draft. |
| schematic | [docs/coala-vs-ours-diagram.html](docs/coala-vs-ours-diagram.html) | 2026-10-01 | The same comparison as a drawn schematic rather than prose: CoALA left, ours right, verdict per row. Adds the beat cycle with the absent learning arrow, the classic blackboard-architecture lineage (DENDRAL) that explains why CoALA is shaped the way it is, and Mermaid source. Every `file:line` opened and read before publishing. |
| architecture | [docs/backend-architecture.html](docs/backend-architecture.html) | 2026-10-01 | How the cabin agent actually works, as three bands: what the captain authors on disk, the Python process, the browser. One beat end to end, the chat path precisely, and four things currently wrong — the persona's declared seat preference, the unwritten prompts, the confirmed prompt write-back, and the chat channel that instrumentation shares with stimulus. |

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
every Sunday at 09:00 -- i.e. 1 day before the Monday weekly refresh -- and
shows a desktop toast pointing at this repo.