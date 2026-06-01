# Topic 4 Pet Translator Demo

This project is a reproducible demo for the experimental final-project topic:
**Pet Translation Device**.

It does not claim to literally understand animal language. Instead, it shows a
serious engineering pipeline:

1. Simulated collar audio event
2. Lightweight audio feature extraction
3. Transparent pet-sound classification
4. LLM-style behavior interpretation
5. Mobile chat UI synchronization

The default mode runs without GPU, internet access, model downloads, or API keys.

## Quick Start

Run the stdlib-only smoke test:

```bash
cd project/topic4_pet_translator_demo
python3 scripts/smoke_test.py
```

Run the CLI:

```bash
PYTHONPATH=src python3 -m pet_translator_demo.cli run --config configs/demo_scenarios.json --mock
```

The command writes:

- `outputs/demo_results.json`
- `outputs/demo_results.csv`
- `outputs/run_summary.md`

Open the UI directly:

```text
web/index.html
```

Optional API server:

```bash
pip install -r requirements.txt
PYTHONPATH=src python3 -m pet_translator_demo.api
```

Then open `web/index.html`. The UI will call `http://127.0.0.1:8004/translate/{scenario_id}`
when the backend is running, and fall back to built-in mock data otherwise.

## Architecture

```text
configs/demo_scenarios.json
        |
        v
AudioFeatureExtractor
        |
        v
PetSoundClassifier
        |
        v
PetBehaviorInterpreter
        |
        v
TranslationPipeline -> JSON/CSV/Summary -> Web UI
```

## Why This Is More Than a Toy

- The classifier exposes evidence and confidence instead of only a funny sentence.
- The pipeline is deterministic, testable, and reproducible.
- The UI is separated from the backend contract.
- Real models can be added behind the same interfaces:
  - `AudioFeatureExtractor`
  - `PetSoundClassifier`
  - `PetBehaviorInterpreter`
  - `TranslationPipeline`

## Suggested Real Extensions

- Replace mock features with Librosa Mel-spectrograms.
- Compare YAMNet, AST, and a small CNN on animal-sound datasets.
- Add RAG with pet profile, breed notes, owner history, and vet-safe cautions.
- Quantize the classifier and benchmark edge-device latency.
- Add a human review workflow for uncertain classifications.

## Submission Checklist

- English video, at least 10 minutes
- Source code folder
- `CONTRIBUTIONS.md`
- `REPOSITORY.md`
- Demo outputs from `outputs/`
- Zip uploaded to Google Drive
- Private WeChat or email message containing only the sharing URL
