"""Generate endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, Optional

from backend.generation.pipeline import generate_candidates as generate_from_preset
from backend.integration.generation_service import generate_candidates as generate_from_engine
from backend.integration.evaluation_service import rank_candidates

router = APIRouter()


class GenerateRequest(BaseModel):
    preset_name: Optional[str] = None
    engine: Optional[str] = None
    input_text: str = "Untitled"
    seed: int = 0
    parameters: Optional[Dict[str, Any]] = None


@router.post("")
def generate(req: GenerateRequest):
    """Generate candidates. Use engine for direct engine, preset_name for preset-based."""
    if req.engine:
        settings = req.parameters or {}
        settings.setdefault("input_text", req.input_text)
        settings.setdefault("seed", req.seed)
        result = generate_from_engine(req.engine, settings)
        ranked = rank_candidates(result["candidates"], finalist_count=5)
        return {
            "candidates": result["candidates"],
            "ranked": ranked,
            "engine": result["engine"],
            "input_text": result["input_text"],
            "seed": result["seed"],
        }
    if req.preset_name:
        return generate_from_preset(req.preset_name, req.input_text, req.seed)
    return {"error": "Provide engine or preset_name", "candidates": []}
