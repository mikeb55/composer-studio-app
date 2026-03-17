"""
Metadata store — Save run metadata (engine, prompt, seed, candidates, exports).
"""

import json
import os
from typing import Any, Dict, List, Optional


def save_run_metadata_full(
    run_path: str,
    *,
    preset_name: Optional[str] = None,
    engine: Optional[str] = None,
    input_text: Optional[str] = None,
    seed: Optional[int] = None,
    candidates: Optional[List[Any]] = None,
    selected_candidate: Optional[Any] = None,
    export_paths: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Save full run metadata for project history.
    """
    meta_dir = os.path.join(run_path, "metadata")
    os.makedirs(meta_dir, exist_ok=True)
    data: Dict[str, Any] = {}
    if preset_name is not None:
        data["preset_name"] = preset_name
    if engine is not None:
        data["engine"] = engine
    if input_text is not None:
        data["input_text"] = input_text
    if seed is not None:
        data["seed"] = seed
    if candidates is not None:
        data["candidates"] = candidates
    if selected_candidate is not None:
        data["selected_candidate"] = selected_candidate
    if export_paths is not None:
        data["export_paths"] = export_paths
    meta_path = os.path.join(meta_dir, "run_metadata.json")
    existing: Dict[str, Any] = {}
    if os.path.isfile(meta_path):
        try:
            with open(meta_path, encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    existing.update(data)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)
    return {"path": meta_path}
