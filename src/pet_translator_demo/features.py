"""Audio feature extraction with a stdlib-only mock path."""

from __future__ import annotations

import math
import wave
from pathlib import Path

from .models import AudioFeatures, Scenario


class AudioFeatureExtractor:
    """Extract lightweight features from a scenario or a WAV file.

    The mock path is deterministic and requires no third-party packages. If a
    PCM WAV file exists, a simple stdlib reader computes real duration, energy,
    and zero-crossing rate so the demo can be upgraded with recorded samples.
    """

    def extract(self, scenario: Scenario, mock: bool = True) -> AudioFeatures:
        if not mock and scenario.audio_path and scenario.audio_path.exists():
            return self._extract_wav(scenario.audio_path)
        return self._extract_mock(scenario)

    def _extract_mock(self, scenario: Scenario) -> AudioFeatures:
        signal = scenario.mock_signal
        duration = signal.get("duration_seconds", 1.5)
        energy = signal.get("energy", 0.4)
        zcr = signal.get("zero_crossing_rate", 0.12)
        centroid = signal.get("spectral_centroid_hz", 1400.0)
        mel_seed = [energy, zcr, min(centroid / 4000.0, 1.0), min(duration / 5.0, 1.0)]
        mock_mel = [
            max(0.0, min(1.0, value + math.sin(index + duration) * 0.03))
            for index, value in enumerate(mel_seed * 2)
        ]
        return AudioFeatures(duration, energy, zcr, centroid, mock_mel)

    def _extract_wav(self, audio_path: Path) -> AudioFeatures:
        with wave.open(str(audio_path), "rb") as handle:
            frames = handle.readframes(handle.getnframes())
            frame_rate = handle.getframerate()
            sample_width = handle.getsampwidth()
            channels = handle.getnchannels()

        if sample_width != 2:
            raise ValueError("Only 16-bit PCM WAV files are supported by the stdlib extractor.")

        samples = []
        for offset in range(0, len(frames), sample_width * channels):
            sample_bytes = frames[offset : offset + sample_width]
            samples.append(int.from_bytes(sample_bytes, "little", signed=True) / 32768.0)

        if not samples:
            return AudioFeatures(0.0, 0.0, 0.0, 0.0, [0.0] * 8)

        duration = len(samples) / float(frame_rate)
        energy = sum(abs(sample) for sample in samples) / len(samples)
        crossings = sum(
            1 for previous, current in zip(samples, samples[1:]) if (previous < 0) != (current < 0)
        )
        zcr = crossings / max(len(samples) - 1, 1)
        centroid = 500.0 + zcr * 7000.0
        mock_mel = [min(1.0, energy * (index + 1) / 2.0 + zcr) for index in range(8)]
        return AudioFeatures(duration, energy, zcr, centroid, mock_mel)
