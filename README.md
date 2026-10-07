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
  coala-correlation.html         -- dark directed correlation: every CoALA component paired with ours by an
                                  arrow labelled with the quality of the match, the five learning actions
                                  resolved one by one, and what each difference costs the experiment
  episodic-ten-beats.html        -- ten beats of one parameter end to end, every number produced by running
                                  the shipped EpisodicMemory: the scoring pipeline, what working memory holds
                                  at each beat, what drops out of the window, and a finding that corrected
                                  a prediction
  sim-architecture-math.html      -- the actual arithmetic from persona entry to episode end: the geometric fit
                                  model, first-order lag and exponential decay constants with their time
                                  constants, the retrieval scorer, the 13-event ride script, the hard limits
                                  with their geometric derivation, and the MDMT scoring
  backend-architecture.html      -- whiteboard map of the whole cabin-agent-sim backend: what the
                                  captain authors on disk, the Python process, the browser, one beat
                                  end to end, the chat path, and what is currently wrong
  data-flow.html                  -- dark directed graph of one beat: six steps down the spine, every
                                  arrow labelled with what is actually sent, the browser and authored
                                  files on the left, the model and hard limits on the right, and the
                                  three arrows that are absent
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
| data flow | [docs/data-flow.html](docs/data-flow.html) | 2026-10-01 | The backend as a directed graph rather than a static picture. One beat down the spine in six steps, every arrow labelled with what is actually sent across it, the browser and authored files in the left lane, the model and hard limits in the right lane. The only arrow pointing backwards is episodic retrieval — the whole of what the agent remembers. Closes with the three arrows that are absent, and why each is absent. |
| correlation | [docs/coala-correlation.html](docs/coala-correlation.html) | 2026-10-01 | Every component of CoALA paired with the cabin agent's counterpart by an arrow labelled with the quality of the match, with the paper retrieved and re-read rather than recalled. Resolves the paper's five learning actions one by one — one present, four absent — and corrects the earlier count that treated learning as a single item. Also records two divergences the earlier pages missed: retrieval is a *chosen* action in CoALA but automatic in ours, and the decision procedure is a component CoALA deliberately leaves unspecified while we close it by making the model the sole decider. |
| ten beats | [docs/episodic-ten-beats.html](docs/episodic-ten-beats.html) | 2026-10-02 | One parameter handled end to end — a passenger gets in, raises the cushion in two steps, finds the top of the rail is right, and holds it. Ten beats, every number produced by importing `cabin_sim.memory` and calling the real `write`/`decay`/`score`/`retrieve`. Shows the scoring pipeline, the store growing to nine while the window holds six, and which episodes drop out. **Corrects a prediction:** the crowding failure I expected does not happen, because importance does not decay. Records the worse finding it uncovered — the discovery survives only on a self-reported importance value, and its recency contributes 0.0002 of its 0.4402 total. |

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