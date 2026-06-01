"""Optional FastAPI server for the demo UI."""

from __future__ import annotations

from pathlib import Path

from .config import load_scenarios
from .pipeline import TranslationPipeline


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs" / "demo_scenarios.json"


def create_app():
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
    except ImportError as exc:
        raise RuntimeError(
            "FastAPI is optional. Install requirements.txt to run the API server."
        ) from exc

    app = FastAPI(title="Topic 4 Pet Translator Demo")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    scenarios = {scenario.id: scenario for scenario in load_scenarios(CONFIG_PATH)}
    pipeline = TranslationPipeline()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/scenarios")
    def list_scenarios() -> list[dict[str, str]]:
        return [
            {"id": scenario.id, "title": scenario.title, "pet": scenario.pet.name}
            for scenario in scenarios.values()
        ]

    @app.post("/translate/{scenario_id}")
    def translate(scenario_id: str) -> dict:
        scenario = scenarios.get(scenario_id)
        if scenario is None:
            raise HTTPException(status_code=404, detail="Unknown scenario id")
        return pipeline.run(scenario, mock=True).as_dict()

    return app


app = create_app()


def main() -> None:
    try:
        import uvicorn
    except ImportError as exc:
        raise RuntimeError("Install uvicorn from requirements.txt to run the API server.") from exc
    uvicorn.run("pet_translator_demo.api:app", host="127.0.0.1", port=8004, reload=False)


if __name__ == "__main__":
    main()
