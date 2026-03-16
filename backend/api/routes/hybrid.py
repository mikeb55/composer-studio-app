"""Hybrid generation endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from backend.integration.hybrid_runtime_adapter import generate_hybrid
from backend.integration.evaluation_service import evaluate_and_rank

router = APIRouter()


class HybridGenerateRequest(BaseModel):
    engine_roles: Dict[str, str]
    parameters: Optional[Dict[str, Any]] = None


@router.post("/generate")
def hybrid_generate(req: HybridGenerateRequest):
    candidates = generate_hybrid(req.engine_roles, req.parameters)
    ranked = evaluate_and_rank(candidates)
    finalist_count = (req.parameters or {}).get("finalist_count", 5)
    return {
        "candidates": candidates,
        "ranked": ranked,
        "finalists": ranked[:finalist_count],
    }
