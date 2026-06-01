"""LLM-style behavior interpretation for classified pet sounds."""

from __future__ import annotations

from .models import Classification, Scenario


class PetBehaviorInterpreter:
    def translate(self, scenario: Scenario, classification: Classification) -> str:
        raise NotImplementedError


class MockLLMBehaviorInterpreter(PetBehaviorInterpreter):
    """A deterministic stand-in for an LLM prompt chain."""

    TEMPLATES = {
        "bark_alert": "Human, I have detected suspicious activity near {context}. Please investigate while I remain extremely brave.",
        "meow_hungry": "Esteemed food provider, my bowl situation near {context} requires urgent executive attention.",
        "purr_happy": "Your service is acceptable. Continue the current comfort protocol near {context}.",
        "whine_anxious": "I am not panicking, but I would appreciate emotional backup around {context}.",
        "chirp_curious": "Interesting discovery at {context}. I request permission to inspect it dramatically.",
        "unknown_review_needed": "I made a sound that your current model cannot explain. Please review the audio before making claims.",
    }

    def translate(self, scenario: Scenario, classification: Classification) -> str:
        template = self.TEMPLATES[classification.label]
        history_hint = self._history_hint(scenario.recent_history)
        personality = scenario.pet.personality.lower()
        line = template.format(context=scenario.context)
        return f"{scenario.pet.name}: {line} {history_hint} Personality filter: {personality}."

    def _history_hint(self, recent_history: list[str]) -> str:
        if not recent_history:
            return "No prior context was available."
        return "Memory says: " + " | ".join(recent_history[-2:])
