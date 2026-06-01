"""Command line interface for the pet translator demo."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_scenarios
from .io import write_outputs
from .pipeline import TranslationPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Topic 4 pet translator demo.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run all configured scenarios.")
    run_parser.add_argument("--config", type=Path, required=True, help="Path to demo_scenarios.json")
    run_parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    run_parser.add_argument("--mock", action="store_true", help="Use deterministic mock audio features.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        scenarios = load_scenarios(args.config)
        pipeline = TranslationPipeline()
        results = pipeline.run_all(scenarios, mock=args.mock)
        write_outputs(results, args.output_dir)
        print(f"Wrote {len(results)} scenario results to {args.output_dir}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
