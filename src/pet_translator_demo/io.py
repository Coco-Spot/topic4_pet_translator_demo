"""Output writers for demo results."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import TranslationResult


CSV_FIELDS = [
    "scenario_id",
    "pet_name",
    "species",
    "label",
    "confidence",
    "duration_seconds",
    "energy",
    "zero_crossing_rate",
    "translation",
]


def write_outputs(results: list[TranslationResult], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(results, output_dir / "demo_results.json")
    write_csv(results, output_dir / "demo_results.csv")
    write_summary(results, output_dir / "run_summary.md")


def write_json(results: list[TranslationResult], path: Path) -> None:
    payload = [result.as_dict() for result in results]
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(results: list[TranslationResult], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "scenario_id": result.scenario_id,
                    "pet_name": result.pet["name"],
                    "species": result.pet["species"],
                    "label": result.classification.label,
                    "confidence": f"{result.classification.confidence:.3f}",
                    "duration_seconds": f"{result.features.duration_seconds:.3f}",
                    "energy": f"{result.features.energy:.4f}",
                    "zero_crossing_rate": f"{result.features.zero_crossing_rate:.4f}",
                    "translation": result.translation,
                }
            )


def write_summary(results: list[TranslationResult], path: Path) -> None:
    lines = [
        "# Pet Translator Demo Run Summary",
        "",
        f"Total scenarios: {len(results)}",
        "",
        "| Scenario | Pet | Classification | Confidence | Translation |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for result in results:
        lines.append(
            "| {scenario} | {pet} | {label} | {confidence:.3f} | {translation} |".format(
                scenario=result.scenario_id,
                pet=result.pet["name"],
                label=result.classification.label,
                confidence=result.classification.confidence,
                translation=result.translation.replace("|", "/"),
            )
        )
    lines.extend(["", f"Safety note: {results[0].safety_note if results else 'N/A'}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
