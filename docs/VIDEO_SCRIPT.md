# English Video Script

Target length: 10 to 12 minutes.

## 0:00-1:00 Opening

Introduce the project: a playful but technically honest pet translator demo.
State the key claim: the system does not decode secret pet language; it builds a
reproducible audio-to-interpretation pipeline.

## 1:00-2:00 Motivation

Show the product concept: a collar captures sounds, a phone receives events, and
the owner sees a chat-like translation. Explain why this is fun, fancy, and
useful for studying AI system design.

## 2:00-3:30 System Architecture

Walk through the five stages:

1. Simulated collar audio event
2. Feature extraction
3. Pet sound classification
4. LLM-style behavior interpretation
5. Mobile chat UI

Emphasize deterministic mock mode for reproducibility.

## 3:30-5:00 Audio and Model Design

Explain the features: duration, energy, zero-crossing rate, spectral centroid,
and mock Mel summary. Show how the transparent classifier maps those features to
labels such as `bark_alert`, `meow_hungry`, `purr_happy`, and `whine_anxious`.

## 5:00-6:30 LLM Interpretation

Explain how the interpreter combines:

- classification label
- pet profile
- recent history
- scene context

Show examples of generated messages. Discuss why evidence and safety notes are
important.

## 6:30-8:00 Live Demo

Run:

```bash
python3 scripts/smoke_test.py
PYTHONPATH=src python3 -m pet_translator_demo.cli run --config configs/demo_scenarios.json --mock
```

Open the web UI and trigger several scenarios. Show JSON, CSV, and summary
outputs.

## 8:00-9:30 Engineering Quality

Show tests, API contract, modular interfaces, and how each team member committed
a meaningful subsystem. Explain how real models can replace mock components
without changing the UI contract.

## 9:30-10:30 Limitations

Discuss:

- animal sounds are ambiguous
- context matters
- LLMs can over-personify
- the system is for entertainment and research, not medical decisions

## 10:30-11:30 Future Work

Mention Librosa features, YAMNet or AST, edge-device benchmarking, RAG with pet
profiles, and uncertainty-aware human review.

## 11:30-12:00 Closing

Summarize the contribution: a fun demo with a serious engineering pipeline,
clear uncertainty, reproducible outputs, and a strong six-person workload split.
