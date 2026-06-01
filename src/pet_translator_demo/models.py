"""Shared dataclasses for the pet translator demo."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PetProfile:
    name: str
    species: str
    breed: str
    personality: str
    owner_notes: str


@dataclass(frozen=True)
class Scenario:
    id: str
    title: str
    audio_path: Path | None
    pet: PetProfile
    expected_sound: str
    context: str
    recent_history: list[str]
    mock_signal: dict[str, float]


@dataclass(frozen=True)
class AudioFeatures:
    duration_seconds: float
    energy: float
    zero_crossing_rate: float
    spectral_centroid_hz: float
    mock_mel_summary: list[float] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "duration_seconds": round(self.duration_seconds, 3),
            "energy": round(self.energy, 4),
            "zero_crossing_rate": round(self.zero_crossing_rate, 4),
            "spectral_centroid_hz": round(self.spectral_centroid_hz, 2),
            "mock_mel_summary": [round(value, 4) for value in self.mock_mel_summary],
        }


@dataclass(frozen=True)
class Classification:
    label: str
    confidence: float
    evidence: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "confidence": round(self.confidence, 3),
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class TranslationResult:
    scenario_id: str
    pet: dict[str, str]
    input_context: str
    features: AudioFeatures
    classification: Classification
    translation: str
    safety_note: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "pet": self.pet,
            "input_context": self.input_context,
            "features": self.features.as_dict(),
            "classification": self.classification.as_dict(),
            "translation": self.translation,
            "safety_note": self.safety_note,
        }
