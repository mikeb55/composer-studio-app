"""Project endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from backend.project.project_manager import (
    create_project,
    create_run_folder,
    save_run_metadata,
    list_projects,
)

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


@router.post("")
def create_project_endpoint(req: CreateProjectRequest):
    return create_project(req.project_name, req.base_dir)


@router.post("/run")
def create_run_endpoint(req: CreateRunRequest):
    return create_run_folder(req.project_name, req.run_label)


@router.post("/metadata")
def save_metadata_endpoint(req: SaveMetadataRequest):
    return save_run_metadata(req.run_path, req.preset_name, req.input_text, req.seed)


@router.get("")
def list_projects_endpoint():
    return list_projects()
