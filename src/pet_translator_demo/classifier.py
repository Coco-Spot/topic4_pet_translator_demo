"""Pet sound classification interfaces and deterministic mock model."""

from __future__ import annotations

from .models import AudioFeatures, Classification, Scenario


ALLOWED_LABELS = {
    "bark_alert",
    "meow_hungry",
    "purr_happy",
    "whine_anxious",
    "chirp_curious",
    "unknown_review_needed",
}


class PetSoundClassifier:
    def classify(self, scenario: Scenario, features: AudioFeatures) -> Classification:
        raise NotImplementedError


class HeuristicPetSoundClassifier(PetSoundClassifier):
    """A transparent classifier suitable for demos and tests."""

    def classify(self, scenario: Scenario, features: AudioFeatures) -> Classification:
        species = scenario.pet.species.lower()
        expected = scenario.expected_sound.lower()
        evidence: list[str] = []

        if "bark" in expected or (species == "dog" and features.energy >= 0.58):
            label = "bark_alert"
            evidence.append("high energy pattern consistent with alert barking")
        elif "purr" in expected or (species == "cat" and features.energy < 0.3 and features.zero_crossing_rate < 0.09):
            label = "purr_happy"
            evidence.append("low energy and low zero-crossing rate resemble a purr")
        elif "meow" in expected or (species == "cat" and features.spectral_centroid_hz >= 1700):
            label = "meow_hungry"
            evidence.append("bright spectral centroid suggests a sharp meow")
        elif "whine" in expected or features.duration_seconds > 2.5:
            label = "whine_anxious"
            evidence.append("longer sustained signal resembles a whine")
        elif "chirp" in expected:
            label = "chirp_curious"
            evidence.append("short bright signal resembles curious chirping")
        else:
            label = "unknown_review_needed"
            evidence.append("feature pattern does not strongly match a known class")

        confidence = self._confidence(label, scenario, features)
        evidence.append(f"scenario context: {scenario.context}")
        return Classification(label=label, confidence=confidence, evidence=evidence)

    def _confidence(self, label: str, scenario: Scenario, features: AudioFeatures) -> float:
        base = 0.62
        if label.split("_")[0] in scenario.expected_sound.lower():
            base += 0.18
        if features.energy > 0.55 or features.zero_crossing_rate < 0.08:
            base += 0.08
        if label == "unknown_review_needed":
            base = 0.41
        return min(base, 0.95)
