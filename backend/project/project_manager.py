"""
Project manager — create project, run folder, metadata.
"""

import os
import json
from datetime import datetime
from typing import Any, Dict, List, Optional


def _projects_base() -> str:
    _here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(_here, "projects")


def create_project(project_name: str, base_dir: Optional[str] = None) -> Dict[str, Any]:
    """Create project directory structure."""
    base = base_dir or _projects_base()
    proj_path = os.path.join(base, project_name)
    for d in ["runs", "candidates", "exports", "notes"]:
        os.makedirs(os.path.join(proj_path, d), exist_ok=True)
    return {"project_name": project_name, "path": proj_path}


def create_run_folder(project_name: str, run_label: Optional[str] = None) -> Dict[str, Any]:
    """Create timestamped run folder."""
    base = _projects_base()
    proj_path = os.path.join(base, project_name)
    if not os.path.isdir(proj_path):
        create_project(project_name, base)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    label = run_label or ts
    run_path = os.path.join(proj_path, "runs", label)
    for d in ["compositions_musicxml", "ensemble_musicxml", "lead_sheets_musicxml", "summaries", "metadata"]:
        os.makedirs(os.path.join(run_path, d), exist_ok=True)
    return {"run_path": run_path, "run_label": label}


def save_run_metadata(run_path: str, preset_name: str, input_text: str, seed: int) -> Dict[str, Any]:
    """Save run metadata JSON."""
    meta_path = os.path.join(run_path, "metadata", "run_metadata.json")
    os.makedirs(os.path.dirname(meta_path), exist_ok=True)
    data = {"preset_name": preset_name, "input_text": input_text, "seed": seed}
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return {"path": meta_path}


def list_projects() -> List[str]:
    """List project names."""
    base = _projects_base()
    if not os.path.isdir(base):
        return []
    return [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
