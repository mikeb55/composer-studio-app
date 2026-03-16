"""Generate endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.generation.pipeline import generate_candidates

router = APIRouter()


class GenerateRequest(BaseModel):
    preset_name: str
    input_text: str
    seed: int = 0


@router.post("")
def generate(req: GenerateRequest):
    result = generate_candidates(req.preset_name, req.input_text, req.seed)
    return result
