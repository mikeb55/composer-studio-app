"""Lead sheet / songwriting endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

from backend.songwriting.songwriting_adapter import build_lead_sheet

router = APIRouter()


class LeadSheetRequest(BaseModel):
    compiled_composition: Any
    voice_type: str = "male_tenor"


@router.post("")
def create_leadsheet(req: LeadSheetRequest):
    result = build_lead_sheet(req.compiled_composition, req.voice_type)
    return result
