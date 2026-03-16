"""Tests for guardrail validation."""

import pytest

from backend.validation.style_guard import check_style_fit, check_texture_density, check_asymmetry
from backend.validation.anti_mush_guard import detect_mush
from backend.validation.export_guard import validate_export


def test_detect_mush_valid():
    """Valid candidate passes anti-mush."""
    candidate = {
        "compiled": {"sections": [{"melody_events": [{"pitch": 60 + i} for i in range(16)]}]},
    }
    ok, score, msg = detect_mush(candidate)
    assert ok is True
    assert msg == "OK"


def test_detect_mush_too_few_notes():
    """Too few notes fails."""
    candidate = {"compiled": {"sections": [{"melody_events": [{"pitch": 60}]}]}}
    ok, score, msg = detect_mush(candidate)
    assert ok is False
    assert "few" in msg.lower()


def test_detect_mush_insufficient_variety():
    """Insufficient pitch variety fails."""
    candidate = {
        "compiled": {"sections": [{"melody_events": [{"pitch": 60} for _ in range(10)]}]},
    }
    ok, score, msg = detect_mush(candidate)
    assert ok is False
    assert "variety" in msg.lower()


def test_check_style_fit_valid():
    """Candidate with score passes."""
    candidate = {"compiled": {"sections": []}, "adjusted_score": 8.0}
    ok, score, msg = check_style_fit(candidate)
    assert ok is True


def test_validate_export_safe():
    """Valid candidate gets SAFE status."""
    candidate = {
        "compiled": {"sections": [{"melody_events": [{"pitch": 60 + (i % 7)} for i in range(16)]}]},
        "adjusted_score": 8.0,
    }
    result = validate_export(candidate)
    assert result["status"] == "SAFE"
    assert result["valid"] is True
    assert result["block_export"] is False


def test_validate_export_blocked():
    """Invalid candidate gets BLOCKED."""
    candidate = {"compiled": None}
    result = validate_export(candidate)
    assert result["status"] == "BLOCKED"
    assert result["block_export"] is True
    assert result["valid"] is False


def test_validate_export_blocked_mush():
    """Mush candidate blocks export."""
    candidate = {
        "compiled": {"sections": [{"melody_events": [{"pitch": 60}]}]},
    }
    result = validate_export(candidate)
    assert result["block_export"] is True
    assert "anti_mush" in result["details"]
