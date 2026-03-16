"""
Hybrid runtime adapter — Wrapper for multi-engine hybrid generation.

Uses same registry interface as single-engine adapter.
"""

from typing import Any, Dict, List, Optional

from backend.integration.engine_registry_loader import ensure_engines_loaded


def generate_hybrid_candidates(
    input_text: str = "Untitled",
    count: int = 12,
    seed: int = 0,
    engine_pool: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Generate multiple hybrid candidates with varied engine combinations.
    All engines loaded via registry.
    """
    ensure_engines_loaded()
    from hybrid_engine.hybrid_generator import generate_hybrid_candidates as _generate
    return _generate(
        input_text=input_text,
        count=count,
        seed=seed,
        engine_pool=engine_pool,
    )


def generate_hybrid_candidate(
    melody_engine: str,
    harmony_engine: str,
    counter_engine: Optional[str] = None,
    rhythm_engine: Optional[str] = None,
    input_text: str = "Untitled",
    seed: int = 0,
) -> Dict[str, Any]:
    """
    Generate one hybrid composition from the given engine combination.
    """
    ensure_engines_loaded()
    from hybrid_engine.hybrid_generator import generate_hybrid_candidate as _generate
    return _generate(
        melody_engine=melody_engine,
        harmony_engine=harmony_engine,
        counter_engine=counter_engine,
        rhythm_engine=rhythm_engine,
        input_text=input_text,
        seed=seed,
    )
