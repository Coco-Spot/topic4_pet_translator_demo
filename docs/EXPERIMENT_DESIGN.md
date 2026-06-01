# Experiment Design

## Research Question

Can a small pet-collar style pipeline turn animal sounds into useful, safe, and
entertaining explanations while making its uncertainty visible?

## Baseline Pipeline

The default demo uses deterministic mock scenarios:

- Dog alert bark near the door
- Cat hungry meow near the food bowl
- Cat happy purr during grooming
- Dog anxious whine at the vet

Each run extracts lightweight audio features, predicts a pet state, and generates
an LLM-style chat message with evidence.

## Metrics

- Classification label accuracy against scenario labels
- Confidence calibration by scenario difficulty
- Runtime per event
- Evidence usefulness judged by humans
- Hallucination risk in generated translations
- UI clarity during live demo

## Ablation Ideas

- Features only vs. features plus context
- Classifier output only vs. LLM-style explanation
- Pet profile disabled vs. pet profile enabled
- Mock feature baseline vs. Librosa Mel-spectrogram features
- Heuristic classifier vs. YAMNet or AST

## Failure Cases to Discuss

- Similar sounds may map to different needs depending on context.
- High-confidence output can still be behaviorally wrong.
- LLM text can become too anthropomorphic.
- Real pet welfare decisions should not rely on the demo alone.

## Real-Model Upgrade Path

1. Collect or download animal-sound datasets.
2. Extract Mel-spectrograms with Librosa.
3. Train or fine-tune YAMNet, AST, or a compact CNN.
4. Add a model-backed `PetSoundClassifier`.
5. Benchmark latency and memory on a laptop or phone-like device.
6. Keep the same JSON contract for the frontend.
