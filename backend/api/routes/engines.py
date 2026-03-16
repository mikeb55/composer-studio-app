"""Engines endpoint."""

from fastapi import APIRouter

from backend.engines.engine_adapter import list_engines, get_presets

router = APIRouter()


@router.get("")
def engines_list():
    return list_engines()


@router.get("/presets")
def presets_list():
    return get_presets()
