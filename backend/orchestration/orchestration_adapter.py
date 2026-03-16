"""
Orchestration adapter — call creative-engines orchestration bridge.
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


def orchestrate_composition(
    compiled_composition: Any,
    ensemble_type: str,
    seed: int = 0,
) -> Dict[str, Any]:
    """Orchestrate composition for ensemble."""
    _ensure_ce_path()
    from orchestration_bridge.orchestration_bridge import orchestrate_composition as _orch
    arr = _orch(compiled_composition, ensemble_type, seed)
    return {"ensemble_arrangement": arr, "ensemble_type": ensemble_type}
