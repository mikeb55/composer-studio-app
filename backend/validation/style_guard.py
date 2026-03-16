"""
Style guard — Style-fit score threshold, texture density sanity, asymmetry enforcement.
"""

from typing import Any, Dict, Tuple


def check_style_fit(candidate: Dict[str, Any]) -> Tuple[bool, float, str]:
    """
    Check style-fit score threshold.
    Returns (pass, score, message).
    """
    if not candidate:
        return False, 0.0, "No candidate"
    compiled = candidate.get("compiled")
    if not compiled:
        return False, 0.0, "No composition"
    raw = candidate.get("style_fit_score")
    if raw is not None:
        score = float(raw) / 10.0 if raw > 1 else float(raw)
    else:
        adj = candidate.get("adjusted_score")
        score = (float(adj) / 10.0) if adj is not None else 0.5
    threshold = 0.3
    if score >= 0.7:
        return True, score, "OK"
    if score >= threshold:
        return True, score, "Acceptable"
    return False, score, f"Style fit below threshold ({score:.2f} < {threshold})"


def check_texture_density(candidate: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Texture density sanity check.
    Returns (pass, message).
    """
    if not candidate:
        return False, "No candidate"
    compiled = candidate.get("compiled")
    if not compiled:
        return True, "OK"
    notes = _count_notes(compiled)
    if notes > 2000:
        return False, "Texture density too high"
    if notes < 4:
        return False, "Insufficient content"
    return True, "OK"


def check_asymmetry(candidate: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Asymmetry enforcement — do not flag asymmetric as bad.
    Returns (pass, message).
    """
    if not candidate:
        return False, "No candidate"
    return True, "OK"


def _count_notes(obj: Any) -> int:
    """Count note-like objects."""
    if isinstance(obj, dict):
        if "pitch" in obj:
            return 1
        total = 0
        for k, v in obj.items():
            if k in ("notes", "events", "melody_events", "counterline_events"):
                if isinstance(v, list):
                    total += len(v)
            else:
                total += _count_notes(v)
        return total
    if isinstance(obj, list):
        return sum(_count_notes(x) for x in obj)
    if hasattr(obj, "sections"):
        total = 0
        for s in obj.sections:
            total += _count_notes(getattr(s, "melody_events", []))
            mb = getattr(s, "melody_blueprint", None)
            if mb:
                total += len(getattr(mb, "intervals", []) or []) + len(getattr(mb, "pitches", []) or [])
        return total
    if hasattr(obj, "melody_events"):
        return _count_notes(getattr(obj, "melody_events", []))
    return 0
