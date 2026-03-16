"""Validation endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict

from backend.validation.export_guard import validate_export

router = APIRouter()


class ValidateRequest(BaseModel):
    candidate: Dict[str, Any]


@router.post("/export")
def validate_export_endpoint(req: ValidateRequest):
    return validate_export(req.candidate)
