"""
Songwriting adapter — call creative-engines songwriting bridge.
"""

import os
import sys
from typing import Any, Dict

def _ensure_ce_path():
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


def build_lead_sheet(compiled_composition: Any, voice_type: str = "male_tenor") -> Dict[str, Any]:
    """Build lead sheet from composition."""
    _ensure_ce_path()
    from songwriting_bridge.songwriting_bridge import build_lead_sheet_from_composition
    lead = build_lead_sheet_from_composition(compiled_composition, voice_type)
    return {"lead_sheet": lead, "voice_type": voice_type}
