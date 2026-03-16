"""
Engine adapter — call creative-engines.
"""

import os
import sys
from typing import Any, Dict, List, Optional

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


def generate_from_engine(engine_name: str, input_text: str, seed: int = 0) -> Dict[str, Any]:
    """Generate from single engine."""
    _ensure_ce_path()
    from shared_composer.engine_registry import get_engine, ensure_engines_loaded
    ensure_engines_loaded()
    eng = get_engine(engine_name)
    ir = eng.generate_ir(input_text, mode="title", seed=seed)
    compiled = eng.compile_from_ir(ir)
    return {"compiled": compiled, "melody_engine": engine_name, "harmony_engine": engine_name}


def generate_hybrid(
    input_text: str,
    count: int = 8,
    seed: int = 0,
    melody_engine: Optional[str] = None,
    harmony_engine: Optional[str] = None,
    counter_engine: Optional[str] = None,
    rhythm_engine: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Generate hybrid candidates."""
    _ensure_ce_path()
    from hybrid_engine.hybrid_generator import generate_hybrid_candidates
    return generate_hybrid_candidates(
        input_text=input_text,
        count=count,
        seed=seed,
    )


def evaluate_candidates(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rank candidates using composition evaluator."""
    _ensure_ce_path()
    from hybrid_engine.hybrid_ranker import rank_hybrid_candidates
    return rank_hybrid_candidates(candidates)


def list_engines() -> List[str]:
    """List available engines."""
    _ensure_ce_path()
    from shared_composer.engine_registry import list_engines as _list, ensure_engines_loaded
    ensure_engines_loaded()
    return _list()


def get_presets() -> List[str]:
    """List preset names."""
    _ensure_ce_path()
    from composer_studio.studio_presets import list_presets
    return list_presets()
