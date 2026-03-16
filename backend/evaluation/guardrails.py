"""
Guardrails — mush detector, style fit, asymmetry check.
"""

from typing import Any, Dict, List, Tuple


def mush_detector(compiled: Any) -> Tuple[bool, float, str]:
    """
    Detect generic/mush output.
    Returns (pass, score, message).
    """
    if not compiled:
        return False, 0.0, "No composition"
    # Minimal heuristic: check for variety
    notes = _extract_notes(compiled)
    if len(notes) < 8:
        return False, 0.3, "Too few notes"
    pitches = [n for n in notes if isinstance(n, (int, float)) or (isinstance(n, dict) and "pitch" in n)]
    if len(set(pitches)) < 4:
        return False, 0.4, "Insufficient pitch variety"
    return True, 0.0, "OK"


def style_fit_check(compiled: Any, preset_name: str) -> Tuple[bool, float, str]:
    """
    Check style fit.
    Returns (pass, score, message).
    """
    if not compiled:
        return False, 0.0, "No composition"
    # Placeholder: pass if we have structure
    return True, 0.0, "OK"


def asymmetry_check(compiled: Any) -> Tuple[bool, float, str]:
    """
    Preserve asymmetry — do not flag asymmetric as bad.
    Returns (pass, score, message).
    """
    if not compiled:
        return False, 0.0, "No composition"
    return True, 0.0, "OK"


def _extract_notes(compiled: Any) -> List:
    """Extract note-like objects from compiled composition."""
    out = []
    if isinstance(compiled, dict):
        for k, v in compiled.items():
            if k in ("notes", "events", "parts"):
                if isinstance(v, list):
                    out.extend(v)
            else:
                out.extend(_extract_notes(v))
    elif isinstance(compiled, list):
        for x in compiled:
            out.extend(_extract_notes(x))
    return out


def run_guardrails(
    compiled: Any,
    preset_name: str,
    style_fit_threshold: float = 0.5,
    anti_mush_threshold: float = 0.5,
) -> Dict[str, Any]:
    """
    Run all guardrails.
    Returns dict with pass, warnings, blocks.
    """
    results = {}
    mush_ok, mush_score, mush_msg = mush_detector(compiled)
    if not mush_ok:
        results["mush"] = {"pass": False, "score": mush_score, "message": mush_msg}
    else:
        results["mush"] = {"pass": True, "score": 1.0, "message": mush_msg}
    style_ok, style_score, style_msg = style_fit_check(compiled, preset_name)
    results["style_fit"] = {"pass": style_ok, "score": style_score, "message": style_msg}
    asym_ok, _, asym_msg = asymmetry_check(compiled)
    results["asymmetry"] = {"pass": asym_ok, "message": asym_msg}
    all_pass = mush_ok and style_ok and asym_ok
    return {
        "pass": all_pass,
        "results": results,
        "warnings": [m for m in [mush_msg, style_msg] if m and m != "OK"],
        "block_export": not all_pass,
    }
