"""Configuration loading for demo scenarios."""

from __future__ import annotations

import json
from pathlib import Path

from .models import PetProfile, Scenario


def load_scenarios(path: Path) -> list[Scenario]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    base_dir = path.parent
    scenarios: list[Scenario] = []
    for item in payload["scenarios"]:
        pet_payload = item["pet"]
        pet = PetProfile(
            name=pet_payload["name"],
            species=pet_payload["species"],
            breed=pet_payload["breed"],
            personality=pet_payload["personality"],
            owner_notes=pet_payload["owner_notes"],
        )
        raw_audio_path = item.get("audio_path")
        audio_path = (base_dir / raw_audio_path).resolve() if raw_audio_path else None
        scenarios.append(
            Scenario(
                id=item["id"],
                title=item["title"],
                audio_path=audio_path,
                pet=pet,
                expected_sound=item["expected_sound"],
                context=item["context"],
                recent_history=list(item.get("recent_history", [])),
                mock_signal={key: float(value) for key, value in item["mock_signal"].items()},
            )
        )
    return scenarios
