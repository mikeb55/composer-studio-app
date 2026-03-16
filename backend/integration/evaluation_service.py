"""
Evaluation service — Requests scoring from engine-side evaluation system,
returns ranked candidates to the UI.
"""

from typing import Any, Dict, List

from backend.integration.engine_registry_loader import ensure_engines_loaded


def evaluate_and_rank(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Request scoring from creative-engines evaluation system.
    Returns ranked candidates (best first) with scores attached.
    """
    ensure_engines_loaded()
    from hybrid_engine.hybrid_ranker import rank_hybrid_candidates
    ranked = rank_hybrid_candidates(candidates)
    return _candidates_to_ui_format(ranked)


def _candidates_to_ui_format(ranked: List[Any]) -> List[Dict[str, Any]]:
    """Convert HybridCandidate objects to dicts for UI consumption."""
    out = []
    for c in ranked:
        result = getattr(c, "compiled_result", c)
        if isinstance(result, dict):
            base = result.copy()
        else:
            base = {
                "compiled": getattr(result, "compiled", None) if result else None,
                "melody_engine": getattr(c, "melody_engine", ""),
                "harmony_engine": getattr(c, "harmony_engine", ""),
                "counter_engine": getattr(c, "counter_engine", None),
                "rhythm_engine": getattr(c, "rhythm_engine", None),
            }
        base["base_score"] = getattr(c, "base_score", 0.0)
        base["style_fit_score"] = getattr(c, "style_fit_score", 0.0)
        base["adjusted_score"] = getattr(c, "adjusted_score", 0.0)
        out.append(base)
    return out


def rank_candidates(
    candidates: List[Dict[str, Any]],
    finalist_count: int = 5,
) -> List[Dict[str, Any]]:
    """
    Rank candidates and return top N for UI.
    """
    ranked = evaluate_and_rank(candidates)
    return ranked[:finalist_count]
