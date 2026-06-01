# Team Contributions

Use this file to keep the six-person contribution record clear for GitHub
history inspection.

| Member | Role | Main Deliverables | Suggested Commit Scope | Workload |
| --- | --- | --- | --- | ---: |
| Member 1 | Audio & Edge Engineer | Mock collar stream, audio feature extraction, sample scenarios | `features.py`, `configs/demo_scenarios.json`, audio notes | 15% |
| Member 2 | AI Model Researcher | Classifier interface, heuristic baseline, real-model comparison notes | `classifier.py`, tests, model benchmark table | 20% |
| Member 3 | LLM & Prompt Engineer | Behavior interpreter, prompt templates, pet memory design | `interpreter.py`, prompt examples, failure analysis | 15% |
| Member 4 | Mobile UI Developer | Phone-style chat UI, waveform animation, frontend contract | `web/index.html`, `web/styles.css`, `web/app.js` | 15% |
| Member 5 | System Integrator | CLI/API integration, Docker, smoke test, output writers | `pipeline.py`, `cli.py`, `api.py`, `scripts/smoke_test.py` | 15% |
| Member 6 | PM & Video Director | README, workload document, English video script, submission checklist | `README.md`, `CONTRIBUTIONS.md`, `docs/VIDEO_SCRIPT.md` | 20% |

## Commit Strategy

- Each member should create commits under their own GitHub account.
- Commit messages should name the subsystem, for example:
  - `audio: add mock collar feature extraction`
  - `model: add heuristic pet sound classifier`
  - `ui: build phone chat interface`
  - `docs: add English video script`
- Avoid one final giant commit by a single person.
