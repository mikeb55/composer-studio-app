"""
Export guard — Validate candidate before export, block invalid outputs.
"""

from typing import Any, Dict, List

from backend.validation.style_guard import check_style_fit, check_texture_density, check_asymmetry
from backend.validation.anti_mush_guard import detect_mush


def validate_export(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate candidate before export.
    Returns dict with: valid, status (SAFE|WARNING|BLOCKED), reasons, details.
    """
    if not candidate:
        return {
            "valid": False,
            "status": "BLOCKED",
            "reasons": ["No candidate"],
            "details": {},
        }
    details: Dict[str, Any] = {}
    reasons: List[str] = []

    style_ok, style_score, style_msg = check_style_fit(candidate)
    details["style_fit"] = {"pass": style_ok, "score": style_score, "message": style_msg}
    if not style_ok:
        reasons.append(style_msg)

    mush_ok, mush_score, mush_msg = detect_mush(candidate)
    details["anti_mush"] = {"pass": mush_ok, "score": mush_score, "message": mush_msg}
    if not mush_ok:
        reasons.append(mush_msg)

    tex_ok, tex_msg = check_texture_density(candidate)
    details["texture_density"] = {"pass": tex_ok, "message": tex_msg}
    if not tex_ok:
        reasons.append(tex_msg)

    asym_ok, asym_msg = check_asymmetry(candidate)
    details["asymmetry"] = {"pass": asym_ok, "message": asym_msg}
    if not asym_ok:
        reasons.append(asym_msg)

    all_pass = style_ok and mush_ok and tex_ok and asym_ok
    if all_pass:
        status = "SAFE"
    elif not mush_ok or not style_ok:
        status = "BLOCKED"
    else:
        status = "WARNING"

    return {
        "valid": all_pass,
        "block_export": status == "BLOCKED",
        "status": status,
        "reasons": reasons,
        "details": details,
    }
