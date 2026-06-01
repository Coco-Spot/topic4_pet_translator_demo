from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pet_translator_demo.classifier import ALLOWED_LABELS
from pet_translator_demo.config import load_scenarios
from pet_translator_demo.pipeline import TranslationPipeline


def test_pipeline_returns_schema_for_all_scenarios():
    scenarios = load_scenarios(ROOT / "configs" / "demo_scenarios.json")
    results = TranslationPipeline().run_all(scenarios, mock=True)

    assert len(results) == len(scenarios)
    for result in results:
        payload = result.as_dict()
        assert payload["classification"]["label"] in ALLOWED_LABELS
        assert 0 <= payload["classification"]["confidence"] <= 1
        assert payload["classification"]["evidence"]
        assert payload["translation"].startswith(payload["pet"]["name"])
        assert "features" in payload


def test_expected_demo_labels_are_stable():
    scenarios = load_scenarios(ROOT / "configs" / "demo_scenarios.json")
    labels = {
        result.scenario_id: result.classification.label
        for result in TranslationPipeline().run_all(scenarios, mock=True)
    }

    assert labels["dog_door_alert"] == "bark_alert"
    assert labels["cat_empty_bowl"] == "meow_hungry"
    assert labels["cat_sofa_purr"] == "purr_happy"
    assert labels["dog_vet_whine"] == "whine_anxious"
