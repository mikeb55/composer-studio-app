"""
Run history — List and load runs for a project.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


def _projects_base() -> str:
    _here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(_here, "projects")


def list_runs(project_name: str) -> List[Dict[str, Any]]:
    """List runs for a project, newest first."""
    base = _projects_base()
    proj_path = os.path.join(base, project_name)
    runs_path = os.path.join(proj_path, "runs")
    if not os.path.isdir(runs_path):
        return []
    entries = []
    for name in os.listdir(runs_path):
        run_path = os.path.join(runs_path, name)
        if not os.path.isdir(run_path):
            continue
        meta_path = os.path.join(run_path, "metadata", "run_metadata.json")
        meta: Dict[str, Any] = {}
        if os.path.isfile(meta_path):
            try:
                with open(meta_path, encoding="utf-8") as f:
                    meta = json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        # Get mtime for ordering
        mtime = os.path.getmtime(run_path)
        entries.append({
            "run_label": name,
            "run_path": run_path,
            "timestamp": datetime.fromtimestamp(mtime).isoformat(),
            **meta,
        })
    entries.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    return entries


def get_run(run_path: str) -> Optional[Dict[str, Any]]:
    """Load run metadata and structure."""
    if not os.path.isdir(run_path):
        return None
    meta_path = os.path.join(run_path, "metadata", "run_metadata.json")
    meta: Dict[str, Any] = {"run_path": run_path}
    if os.path.isfile(meta_path):
        try:
            with open(meta_path, encoding="utf-8") as f:
                meta.update(json.load(f))
        except (json.JSONDecodeError, OSError):
            pass
    return meta
