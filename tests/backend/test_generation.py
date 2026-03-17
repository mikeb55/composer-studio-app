"""Tests for generation via creative-engines integration."""

import os
import tempfile

import pytest

from backend.integration.engine_registry_loader import ensure_engines_loaded
from backend.integration.engine_runtime_adapter import generate, export_musicxml
from backend.integration.generation_service import generate_candidates
from backend.integration.evaluation_service import rank_candidates


def test_generate_single_engine():
    """Generation works with one engine."""
    ensure_engines_loaded()
    result = generate("wheeler_lyric", "Test theme", seed=0)
    assert "compiled" in result
    assert result.get("melody_engine") == "wheeler_lyric"


def test_generate_candidates():
    """generate_candidates creates candidate set (default 5)."""
    result = generate_candidates("wheeler_lyric", {"input_text": "Test", "seed": 0})
    assert "candidates" in result
    assert len(result["candidates"]) == 5
    assert result["engine"] == "wheeler_lyric"


def test_rank_candidates():
    """rank_candidates returns ranked list."""
    result = generate_candidates("wheeler_lyric", {"input_text": "Test", "seed": 0, "count": 3})
    ranked = rank_candidates(result["candidates"], finalist_count=3)
    assert len(ranked) == 3
    assert "adjusted_score" in ranked[0] or "compiled" in ranked[0]


def test_export_musicxml_path_valid():
    """MusicXML export produces valid path when output_dir given."""
    ensure_engines_loaded()
    result = generate("wheeler_lyric", "Export test", seed=0)
    with tempfile.TemporaryDirectory() as d:
        out = export_musicxml(result, output_dir=d, candidate_id="test1")
        assert isinstance(out, dict)
        assert "musicxml_path" in out
        assert out["musicxml_path"].endswith(".musicxml")
        assert os.path.isfile(out["musicxml_path"])
        with open(out["musicxml_path"]) as f:
            xml = f.read()
        assert "<?xml" in xml or "<score-partwise" in xml
