"""Rank endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Any

from backend.integration.evaluation_service import rank_candidates

router = APIRouter()


class RankRequest(BaseModel):
    candidates: List[Any]
    finalist_count: int = 5


@router.post("")
def rank(req: RankRequest):
    """Rank candidates using creative-engines evaluation. Returns ranked list."""
    return rank_candidates(req.candidates, req.finalist_count)
