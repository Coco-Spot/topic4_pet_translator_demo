"""End-to-end translation pipeline."""

from __future__ import annotations

from .classifier import HeuristicPetSoundClassifier, PetSoundClassifier
from .features import AudioFeatureExtractor
from .interpreter import MockLLMBehaviorInterpreter, PetBehaviorInterpreter
from .models import Scenario, TranslationResult


SAFETY_NOTE = (
    "This is an entertainment and research demo. It classifies sound patterns; "
    "it does not prove literal pet language understanding."
)


class TranslationPipeline:
    def __init__(
        self,
        extractor: AudioFeatureExtractor | None = None,
        classifier: PetSoundClassifier | None = None,
        interpreter: PetBehaviorInterpreter | None = None,
    ) -> None:
        self.extractor = extractor or AudioFeatureExtractor()
        self.classifier = classifier or HeuristicPetSoundClassifier()
        self.interpreter = interpreter or MockLLMBehaviorInterpreter()

    def run(self, scenario: Scenario, mock: bool = True) -> TranslationResult:
        features = self.extractor.extract(scenario, mock=mock)
        classification = self.classifier.classify(scenario, features)
        translation = self.interpreter.translate(scenario, classification)
        return TranslationResult(
            scenario_id=scenario.id,
            pet={
                "name": scenario.pet.name,
                "species": scenario.pet.species,
                "breed": scenario.pet.breed,
            },
            input_context=scenario.context,
            features=features,
            classification=classification,
            translation=translation,
            safety_note=SAFETY_NOTE,
        )

    def run_all(self, scenarios: list[Scenario], mock: bool = True) -> list[TranslationResult]:
        return [self.run(scenario, mock=mock) for scenario in scenarios]
