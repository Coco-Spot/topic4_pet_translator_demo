"""Stdlib-only smoke test for the Topic 4 pet translator demo."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from pet_translator_demo.classifier import ALLOWED_LABELS
from pet_translator_demo.config import load_scenarios
from pet_translator_demo.io import write_outputs
from pet_translator_demo.pipeline import TranslationPipeline


def main() -> int:
    scenarios = load_scenarios(ROOT / "configs" / "demo_scenarios.json")
    results = TranslationPipeline().run_all(scenarios, mock=True)
    if len(results) != len(scenarios):
        print(f"Expected {len(scenarios)} results, got {len(results)}")
        return 1
    for result in results:
        if result.classification.label not in ALLOWED_LABELS:
            print(f"Unexpected label: {result.classification.label}")
            return 1
        if not result.classification.evidence:
            print(f"Missing evidence for {result.scenario_id}")
            return 1
        if not result.translation or result.pet["name"] not in result.translation:
            print(f"Missing pet-specific translation for {result.scenario_id}")
            return 1
    write_outputs(results, ROOT / "outputs")
    print(f"Smoke test passed. Wrote outputs to {ROOT / 'outputs'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
