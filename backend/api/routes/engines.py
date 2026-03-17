"""Engines endpoint."""

from fastapi import APIRouter

from backend.integration.engine_registry_loader import list_engines
from backend.integration.generation_service import list_presets

router = APIRouter()


@router.get("")
def engines_list():
    """Return list of engines from creative-engines registry."""
    return list_engines()


@router.get("/presets")
def presets_list():
    return list_presets()
