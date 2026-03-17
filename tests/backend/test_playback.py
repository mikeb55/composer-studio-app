"""Tests for playback API and service."""

import pytest


def _client():
    try:
        from fastapi.testclient import TestClient
        from backend.api.main import app
        return TestClient(app)
    except RuntimeError:
        pytest.skip("httpx required for TestClient")


def test_playback_stop_returns_status():
    """POST /playback/stop returns sane status."""
    r = _client().post("/playback/stop")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert data.get("state") == "stopped"


def test_playback_pause_returns_status():
    """POST /playback/pause returns sane status."""
    r = _client().post("/playback/pause")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert "state" in data


def test_playback_status_endpoint():
    """GET /playback/status returns status."""
    r = _client().get("/playback/status")
    assert r.status_code == 200
    data = r.json()
    assert "state" in data
    assert data["state"] in ("stopped", "playing", "paused")


def test_playback_play_without_file_returns_error():
    """POST /playback/play without file or musicxml returns error."""
    r = _client().post("/playback/play", json={})
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") in ("error", "playback_not_implemented")
    assert "message" in data or "state" in data


def test_playback_play_with_musicxml_returns_structured_response():
    """POST /playback/play with musicxml returns structured response (may be not_implemented)."""
    r = _client().post("/playback/play", json={
        "musicxml": '<?xml version="1.0"?><score-partwise/>',
    })
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    # Either plays or returns playback_not_implemented
    assert data["status"] in ("playing", "playback_not_implemented", "error")


def test_playback_loop_endpoint():
    """POST /playback/loop sets loop and returns status."""
    r = _client().post("/playback/loop", json={"loop_start": 1, "loop_end": 4})
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert data.get("loop_start") == 1
    assert data.get("loop_end") == 4
