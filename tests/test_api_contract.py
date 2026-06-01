from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pet_translator_demo.config import load_scenarios
from pet_translator_demo.pipeline import TranslationPipeline


def test_translate_payload_matches_frontend_contract():
    scenario = load_scenarios(ROOT / "configs" / "demo_scenarios.json")[0]
    payload = TranslationPipeline().run(scenario, mock=True).as_dict()

    assert set(payload) == {
        "scenario_id",
        "pet",
        "input_context",
        "features",
        "classification",
        "translation",
        "safety_note",
    }
    assert {"name", "species", "breed"} <= set(payload["pet"])
    assert {"label", "confidence", "evidence"} <= set(payload["classification"])
    assert {"duration_seconds", "energy", "zero_crossing_rate", "mock_mel_summary"} <= set(
        payload["features"]
    )
