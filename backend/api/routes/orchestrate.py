"""Orchestrate endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

from backend.orchestration.orchestration_adapter import orchestrate_composition

router = APIRouter()


class OrchestrateRequest(BaseModel):
    compiled_composition: Any
    ensemble_type: str
    seed: int = 0


@router.post("")
def orchestrate(req: OrchestrateRequest):
    result = orchestrate_composition(
        req.compiled_composition,
        req.ensemble_type,
        req.seed,
    )
    return result
