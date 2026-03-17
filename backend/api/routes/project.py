"""Project endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, List, Optional

from backend.project.project_manager import (
    create_project,
    create_run_folder,
    save_run_metadata,
    list_projects,
)
from backend.project.run_history import list_runs, get_run
from backend.project.metadata_store import save_run_metadata_full

router = APIRouter()


class CreateProjectRequest(BaseModel):
    project_name: str
    base_dir: Optional[str] = None


class CreateRunRequest(BaseModel):
    project_name: str
    run_label: Optional[str] = None


class SaveMetadataRequest(BaseModel):
    run_path: str
    preset_name: str
    input_text: str
    seed: int


class SaveRunRequest(BaseModel):
    project_name: str
    run_label: Optional[str] = None
    preset_name: Optional[str] = None
    engine: Optional[str] = None
    input_text: Optional[str] = None
    seed: Optional[int] = None
    candidates: Optional[List[Any]] = None
    selected_candidate: Optional[Any] = None
    export_paths: Optional[List[str]] = None
    musicxml: Optional[str] = None  # If provided, write to run folder


@router.post("")
def create_project_endpoint(req: CreateProjectRequest):
    return create_project(req.project_name, req.base_dir)


@router.post("/create")
def create_project_create_endpoint(req: CreateProjectRequest):
    """Alias for POST /project - create project."""
    return create_project(req.project_name, req.base_dir)


@router.post("/run")
def create_run_endpoint(req: CreateRunRequest):
    return create_run_folder(req.project_name, req.run_label)


@router.post("/run/save")
def save_run_endpoint(req: SaveRunRequest):
    """Create run folder and save full run metadata."""
    import os
    run_result = create_run_folder(req.project_name, req.run_label)
    run_path = run_result["run_path"]
    export_paths = list(req.export_paths) if req.export_paths else []
    if req.musicxml:
        comp_dir = os.path.join(run_path, "compositions_musicxml")
        os.makedirs(comp_dir, exist_ok=True)
        xml_path = os.path.join(comp_dir, "selected.musicxml")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(req.musicxml)
        # Store URL path for frontend (projects/... for /api/projects/... fetch)
        from backend.project.project_manager import _projects_base
        proj_base = _projects_base()
        if xml_path.startswith(proj_base):
            rel = os.path.relpath(xml_path, proj_base).replace("\\", "/")
            export_paths.append(f"projects/{rel}")
        else:
            export_paths.append(xml_path)
    save_run_metadata_full(
        run_path,
        preset_name=req.preset_name,
        engine=req.engine,
        input_text=req.input_text,
        seed=req.seed,
        candidates=req.candidates,
        selected_candidate=req.selected_candidate,
        export_paths=export_paths or None,
    )
    return {**run_result, "metadata_path": f"{run_path}/metadata/run_metadata.json", "export_paths": export_paths}


@router.post("/metadata")
def save_metadata_endpoint(req: SaveMetadataRequest):
    return save_run_metadata(req.run_path, req.preset_name, req.input_text, req.seed)


@router.get("")
def list_projects_endpoint():
    return list_projects()


@router.get("/history/{project_name}")
def get_project_history_endpoint(project_name: str):
    """Get run history for a project."""
    return list_runs(project_name)


@router.get("/{project_name}")
def get_project_endpoint(project_name: str):
    """Get project detail including runs."""
    import os
    from backend.project.project_manager import _projects_base
    base = _projects_base()
    proj_path = os.path.join(base, project_name)
    if not os.path.isdir(proj_path):
        return {"error": "Project not found", "project_name": project_name}
    runs = list_runs(project_name)
    return {
        "project_name": project_name,
        "path": proj_path,
        "runs": runs,
    }
