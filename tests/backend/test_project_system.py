"""Tests for project system: creation, run save, history."""

import json
import os
import tempfile
import uuid

import pytest

from backend.project.project_manager import (
    create_project,
    create_run_folder,
    list_projects,
)
from backend.project.run_history import list_runs, get_run
from backend.project.metadata_store import save_run_metadata_full


def _unique_name():
    return f"test_proj_{uuid.uuid4().hex[:8]}"


def test_create_project():
    """Project creation creates directory structure."""
    with tempfile.TemporaryDirectory() as d:
        result = create_project("test_proj", base_dir=d)
        assert result["project_name"] == "test_proj"
        assert "path" in result
        proj_path = result["path"]
        assert os.path.isdir(proj_path)
        for sub in ["runs", "candidates", "exports", "notes"]:
            assert os.path.isdir(os.path.join(proj_path, sub))


def test_create_run_folder():
    """Run folder creation creates timestamped run."""
    name = _unique_name()
    create_project(name)
    try:
        result = create_run_folder(name, run_label="run1")
        assert result["run_label"] == "run1"
        assert "run_path" in result
        assert os.path.isdir(result["run_path"])
        meta_dir = os.path.join(result["run_path"], "metadata")
        assert os.path.isdir(meta_dir)
    finally:
        _cleanup_project(name)


def test_save_run_metadata_full():
    """Save run metadata writes JSON."""
    name = _unique_name()
    create_project(name)
    try:
        run_result = create_run_folder(name, run_label="run1")
        run_path = run_result["run_path"]
        save_run_metadata_full(
            run_path,
            preset_name="wheeler_lyric",
            input_text="Test",
            seed=42,
            candidates=[{"compiled": {}}],
        )
        meta_path = os.path.join(run_path, "metadata", "run_metadata.json")
        assert os.path.isfile(meta_path)
        with open(meta_path) as f:
            data = json.load(f)
        assert data["preset_name"] == "wheeler_lyric"
        assert data["input_text"] == "Test"
        assert data["seed"] == 42
        assert len(data["candidates"]) == 1
    finally:
        _cleanup_project(name)


def test_list_runs():
    """list_runs returns runs for project."""
    name = _unique_name()
    create_project(name)
    try:
        create_run_folder(name, run_label="run1")
        create_run_folder(name, run_label="run2")
        runs = list_runs(name)
        assert len(runs) >= 2
        labels = {r["run_label"] for r in runs}
        assert "run1" in labels
        assert "run2" in labels
    finally:
        _cleanup_project(name)


def test_get_run():
    """get_run returns run metadata."""
    name = _unique_name()
    create_project(name)
    try:
        run_result = create_run_folder(name, run_label="run1")
        run_path = run_result["run_path"]
        save_run_metadata_full(run_path, preset_name="barry", input_text="Foo")
        run_data = get_run(run_path)
        assert run_data is not None
        assert run_data.get("preset_name") == "barry"
        assert run_data.get("input_text") == "Foo"
    finally:
        _cleanup_project(name)


def _cleanup_project(project_name: str):
    """Remove test project directory."""
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "projects")
    path = os.path.join(base, project_name)
    if os.path.isdir(path):
        import shutil
        shutil.rmtree(path, ignore_errors=True)


def test_project_api_routes():
    """Project API endpoints return sane responses."""
    try:
        from fastapi.testclient import TestClient
    except RuntimeError:
        pytest.skip("httpx required for TestClient")
    from backend.api.main import app
    client = TestClient(app)

    # Create project
    r = client.post("/project/create", json={"project_name": "api_test_proj"})
    assert r.status_code == 200
    data = r.json()
    assert data.get("project_name") == "api_test_proj"

    # Save run
    r = client.post("/project/run/save", json={
        "project_name": "api_test_proj",
        "run_label": "api_run_1",
        "preset_name": "wheeler_lyric",
        "input_text": "API test",
        "seed": 0,
        "musicxml": '<?xml version="1.0"?><score-partwise/>',
    })
    assert r.status_code == 200
    data = r.json()
    assert "run_path" in data
    assert "run_label" in data

    # Get history
    r = client.get("/project/history/api_test_proj")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # Get project
    r = client.get("/project/api_test_proj")
    assert r.status_code == 200
    data = r.json()
    assert data.get("project_name") == "api_test_proj"
    assert "runs" in data
