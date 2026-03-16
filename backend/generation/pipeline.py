"""
Generation pipeline — generate, rank, select finalists.
"""

from typing import Any, Dict, List

from backend.engines.engine_adapter import (
    generate_from_engine,
    generate_hybrid,
    evaluate_candidates,
)
from backend.engines.engine_adapter import _ensure_ce_path


def _get_preset(name: str):
    _ensure_ce_path()
    from composer_studio.studio_presets import get_preset
    return get_preset(name)


def generate_candidates(preset_name: str, input_text: str, seed: int = 0) -> Dict[str, Any]:
    """Generate candidates from preset."""
    preset = _get_preset(preset_name)
    if not preset:
        return {"error": f"Unknown preset: {preset_name}", "candidates": []}
    if preset.engine_mode == "single":
        candidates = []
        for i in range(preset.population_size):
            c = generate_from_engine(preset.melody_engine, input_text, seed + i)
            candidates.append(c)
    else:
        candidates = generate_hybrid(
            input_text,
            count=preset.population_size,
            seed=seed,
        )
    ranked = evaluate_candidates(candidates)
    finalists = ranked[: preset.finalist_count]
    return {
        "preset": preset_name,
        "input_text": input_text,
        "seed": seed,
        "candidates": candidates,
        "ranked": ranked,
        "finalists": finalists,
    }


def rank_candidates(candidates: List[Dict[str, Any]], finalist_count: int = 5) -> List[Dict[str, Any]]:
    """Rank and return top N."""
    ranked = evaluate_candidates(candidates)
    return ranked[:finalist_count]


def select_finalists(ranked: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
    """Select top N finalists."""
    return ranked[:count]
