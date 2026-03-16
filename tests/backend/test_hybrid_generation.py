"""Tests for hybrid generation."""

import pytest

from backend.integration.hybrid_runtime_adapter import generate_hybrid, generate_hybrid_candidate


def test_generate_hybrid_with_engine_roles():
    """Hybrid generation works with explicit engine roles."""
    engine_roles = {
        "form_engine": "wayne_shorter",
        "harmony_engine": "wheeler_lyric",
        "texture_engine": "ligeti_texture",
        "orchestration_engine": "big_band",
        "counterpoint_engine": "",
    }
    parameters = {"input_text": "Test", "seed": 42, "count": 2}
    results = generate_hybrid(engine_roles, parameters)
    assert len(results) == 2
    for c in results:
        assert "compiled" in c
        assert c.get("melody_engine") == "wayne_shorter"
        assert c.get("harmony_engine") == "wheeler_lyric"
        assert c.get("engine_roles") == engine_roles


def test_generate_hybrid_candidate():
    """Single hybrid candidate generation."""
    c = generate_hybrid_candidate(
        melody_engine="wayne_shorter",
        harmony_engine="barry_harris",
        counter_engine=None,
        rhythm_engine="monk",
        input_text="Untitled",
        seed=0,
    )
    assert "compiled" in c
    assert c.get("melody_engine") == "wayne_shorter"
    assert c.get("harmony_engine") == "barry_harris"


def test_generate_hybrid_with_counterpoint():
    """Hybrid with counterpoint engine."""
    engine_roles = {
        "form_engine": "wayne_shorter",
        "harmony_engine": "barry_harris",
        "counterpoint_engine": "andrew_hill",
    }
    results = generate_hybrid(engine_roles, {"count": 1})
    assert len(results) == 1
    assert results[0].get("counter_engine") == "andrew_hill"
