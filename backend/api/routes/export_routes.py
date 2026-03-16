"""Export endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Any, Optional

from backend.export.export_handler import (
    export_musicxml,
    export_lead_sheet,
    export_orchestrated_score,
    export_project_archive,
)

router = APIRouter()


class ExportMusicXMLRequest(BaseModel):
    compiled: Any
    filename: Optional[str] = None


class ExportLeadSheetRequest(BaseModel):
    lead_sheet: Any
    filename: Optional[str] = None


class ExportOrchestratedRequest(BaseModel):
    ensemble_arrangement: Any
    filename: Optional[str] = None


class ExportArchiveRequest(BaseModel):
    project_name: str
    run_path: str
    include: List[str] = ["compositions", "ensemble", "lead_sheets"]


@router.post("/musicxml")
def export_musicxml_endpoint(req: ExportMusicXMLRequest):
    return export_musicxml(req.compiled, req.filename)


@router.post("/lead_sheet")
def export_lead_sheet_endpoint(req: ExportLeadSheetRequest):
    return export_lead_sheet(req.lead_sheet, req.filename)


@router.post("/orchestrated")
def export_orchestrated_endpoint(req: ExportOrchestratedRequest):
    return export_orchestrated_score(req.ensemble_arrangement, req.filename)


@router.post("/archive")
def export_archive_endpoint(req: ExportArchiveRequest):
    return export_project_archive(req.project_name, req.run_path, req.include)
