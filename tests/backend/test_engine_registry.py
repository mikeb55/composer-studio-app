"""Tests for engine registry connection to creative-engines."""

import pytest

from backend.integration.engine_registry_loader import (
    load_registry,
    list_engines,
    get_engine,
    ensure_engines_loaded,
)


def test_load_registry():
    """load_registry() loads creative-engines registry."""
    load_registry()
    engines = list_engines()
    assert isinstance(engines, list)
    assert len(engines) > 0


def test_list_engines():
    """list_engines() returns engine names from registry."""
    ensure_engines_loaded()
    engines = list_engines()
    assert "wayne_shorter" in engines
    assert "wheeler_lyric" in engines
    assert "barry_harris" in engines


def test_get_engine():
    """get_engine() returns engine instance."""
    ensure_engines_loaded()
    eng = get_engine("wayne_shorter")
    assert eng is not None
    assert hasattr(eng, "generate_ir")
    assert hasattr(eng, "compile_from_ir")
    assert hasattr(eng, "export_musicxml")


def test_engine_discovery():
    """Engine discovery works - at least 10 engines."""
    engines = list_engines()
    assert len(engines) >= 10
