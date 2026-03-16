"""
Export handler — MusicXML, lead sheet, orchestrated, archive.
"""

import os
from typing import Any, Dict, List, Optional

def _ensure_ce_path():
    import sys
    _ce = os.environ.get("CREATIVE_ENGINES_PATH")
    if _ce:
        _eng = os.path.join(_ce, "engines") if os.path.isdir(os.path.join(_ce, "engines")) else _ce
        if _eng not in sys.path:
            sys.path.insert(0, _eng)
        return
    _here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _ce_root = os.path.join(_here, "creative-engines")
    _eng = os.path.join(_ce_root, "engines")
    if os.path.isdir(_eng) and _eng not in sys.path:
        sys.path.insert(0, _eng)
        return
    _ce_root = os.path.abspath(os.path.join(_here, "..", "creative-engines"))
    _eng = os.path.join(_ce_root, "engines")
    if os.path.isdir(_eng) and _eng not in sys.path:
        sys.path.insert(0, _eng)


def export_musicxml(compiled: Any, filename: Optional[str] = None) -> Dict[str, Any]:
    """Export composition to MusicXML string. Blocks if guardrails fail."""
    from backend.validation.export_guard import validate_export
    cand = compiled if isinstance(compiled, dict) else {"compiled": compiled}
    validation = validate_export(cand)
    if validation.get("block_export"):
        return {
            "error": "Export blocked by guardrails",
            "status": validation.get("status", "BLOCKED"),
            "reasons": validation.get("reasons", []),
            "musicxml": "",
            "filename": filename or "composition.musicxml",
        }
    _ensure_ce_path()
    from shared_composer.engine_registry import get_engine, ensure_engines_loaded
    ensure_engines_loaded()
    cand = compiled.get("compiled") if isinstance(compiled, dict) else compiled
    mel = compiled.get("melody_engine", "wayne_shorter") if isinstance(compiled, dict) else "wayne_shorter"
    if isinstance(compiled, dict) and (compiled.get("counterline_events") or compiled.get("inner_voice_events")):
        from hybrid_engine.hybrid_musicxml_exporter import export_hybrid_to_musicxml
        xml = export_hybrid_to_musicxml(compiled)
    else:
        eng = get_engine(mel)
        xml = eng.export_musicxml(cand)
    result: Dict[str, Any] = {"musicxml": xml, "filename": filename or "composition.musicxml"}
    result["guardrail_status"] = validation.get("status", "SAFE")
    return result


def export_lead_sheet(lead_sheet: Any, filename: Optional[str] = None) -> Dict[str, str]:
    """Export lead sheet to MusicXML."""
    _ensure_ce_path()
    from songwriting_bridge.lead_sheet_exporter import export_lead_sheet_to_musicxml
    xml = export_lead_sheet_to_musicxml(lead_sheet)
    return {"musicxml": xml, "filename": filename or "lead_sheet.musicxml"}


def export_orchestrated_score(ensemble_arrangement: Any, filename: Optional[str] = None) -> Dict[str, str]:
    """Export orchestrated score to MusicXML."""
    _ensure_ce_path()
    from orchestration_bridge.ensemble_musicxml_exporter import export_ensemble_to_musicxml
    xml = export_ensemble_to_musicxml(ensemble_arrangement)
    return {"musicxml": xml, "filename": filename or "ensemble.musicxml"}


def export_project_archive(
    project_name: str,
    run_path: str,
    include: List[str],
) -> Dict[str, Any]:
    """Create project archive."""
    if not os.path.isdir(run_path):
        return {"error": "Run path not found", "path": run_path}
    # Return paths for frontend to package
    return {
        "project_name": project_name,
        "run_path": run_path,
        "include": include,
        "message": "Use run_path to package files",
    }
