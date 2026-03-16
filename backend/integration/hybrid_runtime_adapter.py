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


def generate_hybrid(
    engine_roles: Dict[str, str],
    parameters: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Generate hybrid composition(s) from explicit engine roles.

    engine_roles example:
        {
            "form_engine": "wayne_shorter",
            "harmony_engine": "wheeler_lyric",
            "texture_engine": "ligeti_texture",
            "orchestration_engine": "big_band",
            "counterpoint_engine": "andrew_hill"
        }

    Maps to creative-engines: form->melody, harmony->harmony,
    texture->rhythm, counterpoint->counter, orchestration stored in metadata.
    """
    ensure_engines_loaded()
    params = parameters or {}
    input_text = params.get("input_text", "Untitled")
    seed = params.get("seed", 0)
    count = params.get("count", 1)

    form = engine_roles.get("form_engine") or "wayne_shorter"
    harmony = engine_roles.get("harmony_engine") or "barry_harris"
    texture = engine_roles.get("texture_engine") or engine_roles.get("orchestration_engine")
    counter = engine_roles.get("counterpoint_engine")

    results: List[Dict[str, Any]] = []
    for i in range(count):
        c = generate_hybrid_candidate(
            melody_engine=form,
            harmony_engine=harmony,
            counter_engine=counter or None,
            rhythm_engine=texture or None,
            input_text=input_text,
            seed=seed + i,
        )
        c["engine_roles"] = engine_roles
        results.append(c)
    return results
