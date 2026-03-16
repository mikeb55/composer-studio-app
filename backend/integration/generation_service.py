"""
Generation service — Coordinates engine selection, generation settings, candidate creation.
"""

from typing import Any, Dict, List, Optional

from backend.integration.engine_registry_loader import ensure_engines_loaded, list_engines
from backend.integration.engine_runtime_adapter import generate as generate_single
from backend.integration.hybrid_runtime_adapter import generate_hybrid_candidates


def _get_preset(preset_name: str) -> Optional[Any]:
    """Load preset from creative-engines composer_studio."""
    ensure_engines_loaded()
    from composer_studio.studio_presets import get_preset
    return get_preset(preset_name)


def list_available_engines() -> List[str]:
    """List engines available via registry."""
    return list_engines()


def list_presets() -> List[str]:
    """List preset names from composer_studio."""
    ensure_engines_loaded()
    from composer_studio.studio_presets import list_presets
    return list_presets()


def create_candidates(
    preset_name: str,
    input_text: str,
    seed: int = 0,
) -> Dict[str, Any]:
    """
    Create candidates from preset.
    Coordinates engine selection, generation settings, candidate creation.
    Returns dict with preset, input_text, seed, candidates (raw, not yet ranked).
    """
    preset = _get_preset(preset_name)
    if not preset:
        return {
            "error": f"Unknown preset: {preset_name}",
            "preset": preset_name,
            "input_text": input_text,
            "seed": seed,
            "candidates": [],
        }
    candidates: List[Dict[str, Any]] = []
    if preset.engine_mode == "single":
        engine_name = preset.melody_engine or "wayne_shorter"
        for i in range(preset.population_size):
            c = generate_single(engine_name, input_text, seed=seed + i)
            candidates.append(c)
    else:
        candidates = generate_hybrid_candidates(
            input_text=input_text,
            count=preset.population_size,
            seed=seed,
        )
    return {
        "preset": preset_name,
        "input_text": input_text,
        "seed": seed,
        "candidates": candidates,
        "preset_config": preset,
    }


def create_single_engine_candidates(
    engine_name: str,
    input_text: str,
    count: int = 8,
    seed: int = 0,
) -> List[Dict[str, Any]]:
    """Create candidates from single engine."""
    return [
        generate_single(engine_name, input_text, seed=seed + i)
        for i in range(count)
    ]


def create_hybrid_candidates(
    input_text: str,
    count: int = 12,
    seed: int = 0,
    engine_pool: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Create hybrid candidates with varied engine combinations."""
    return generate_hybrid_candidates(
        input_text=input_text,
        count=count,
        seed=seed,
        engine_pool=engine_pool,
    )
