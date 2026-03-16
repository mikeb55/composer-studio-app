"""
Anti-mush guard — Detect generic/low-quality output.
"""

from typing import Any, Dict, List, Tuple


def detect_mush(candidate: Dict[str, Any]) -> Tuple[bool, float, str]:
    """
    Detect mush (generic, low-quality) output.
    Returns (pass, score, message).
    """
    if not candidate:
        return False, 0.0, "No candidate"
    compiled = candidate.get("compiled")
    if not compiled:
        return False, 0.0, "No composition"
    notes = _extract_notes(compiled)
    if len(notes) < 8:
        return False, 0.3, "Too few notes"
    pitches = _extract_pitches(notes)
    if len(pitches) < 4:
        return False, 0.4, "Insufficient pitch variety"
    return True, 1.0, "OK"


def _extract_notes(compiled: Any) -> List[Any]:
    """Extract note-like objects from compiled composition."""
    out: List[Any] = []
    if isinstance(compiled, dict):
        if "pitch" in compiled:
            out.append(compiled)
        else:
            for k, v in compiled.items():
                if k in ("notes", "events", "melody_events", "counterline_events", "parts"):
                    if isinstance(v, list):
                        out.extend(v)
                else:
                    out.extend(_extract_notes(v))
    elif isinstance(compiled, list):
        for x in compiled:
            out.extend(_extract_notes(x))
    elif hasattr(compiled, "sections"):
        for sec in compiled.sections:
            out.extend(_extract_notes(getattr(sec, "melody_events", [])))
    elif hasattr(compiled, "melody_events"):
        out.extend(_extract_notes(getattr(compiled, "melody_events", [])))
    return out


def _extract_pitches(notes: List[Any]) -> set:
    """Extract unique pitches from notes."""
    pitches = set()
    for n in notes:
        if isinstance(n, (int, float)):
            pitches.add(int(n) % 12)
        elif isinstance(n, dict):
            p = n.get("pitch")
            if p is not None:
                pitches.add(int(p) % 12)
    return pitches
