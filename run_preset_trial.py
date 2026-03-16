"""
Preset quality trial — Run batch generation across presets, score, and report.
"""
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _get_top_candidate(ranked: List, candidates: List) -> Optional[Dict]:
    """Extract top candidate dict for export."""
    if not ranked:
        return candidates[0] if candidates else None
    top = ranked[0]
    if hasattr(top, "compiled_result"):
        return top.compiled_result if isinstance(top.compiled_result, dict) else top
    return top if isinstance(top, dict) else None


def run_trial(
    preset_name: str,
    input_text: str,
    seed: int = 0,
) -> Dict[str, Any]:
    """Run one preset trial: generate, rank, export top."""
    from backend.generation.pipeline import generate_candidates
    from backend.validation.export_guard import validate_export
    from backend.export.export_handler import export_musicxml

    result: Dict[str, Any] = {
        "preset": preset_name,
        "input_text": input_text,
        "seed": seed,
        "candidate_count": 0,
        "top_score": None,
        "guardrail_status": None,
        "export_ok": False,
        "export_error": None,
        "musicxml_len": 0,
        "error": None,
    }
    try:
        gen = generate_candidates(preset_name, input_text, seed)
        if gen.get("error"):
            result["error"] = gen["error"]
            return result

        candidates = gen.get("candidates", [])
        ranked = gen.get("ranked", [])
        result["candidate_count"] = len(candidates)

        if ranked:
            top = ranked[0]
            result["top_score"] = getattr(top, "adjusted_score", top.get("adjusted_score") if isinstance(top, dict) else None)

        cand = _get_top_candidate(ranked, candidates)
        if cand:
            val = validate_export(cand)
            result["guardrail_status"] = val.get("status")
            exp = export_musicxml(cand)
            result["export_ok"] = exp.get("error") is None
            result["export_error"] = exp.get("error")
            result["musicxml_len"] = len(exp.get("musicxml", ""))
    except Exception as e:
        result["error"] = str(e)
    return result


def run_hybrid_trial(
    engine_roles: Dict[str, str],
    input_text: str,
    seed: int = 0,
) -> Dict[str, Any]:
    """Run hybrid trial with explicit engine roles."""
    from backend.integration.hybrid_runtime_adapter import generate_hybrid
    from backend.integration.evaluation_service import evaluate_and_rank
    from backend.validation.export_guard import validate_export
    from backend.export.export_handler import export_musicxml

    result: Dict[str, Any] = {
        "preset": "hybrid:" + "+".join(f"{k}={v}" for k, v in sorted(engine_roles.items())),
        "input_text": input_text,
        "seed": seed,
        "candidate_count": 0,
        "top_score": None,
        "guardrail_status": None,
        "export_ok": False,
        "export_error": None,
        "musicxml_len": 0,
        "error": None,
    }
    try:
        candidates = generate_hybrid(engine_roles, {"input_text": input_text, "seed": seed, "count": 1})
        result["candidate_count"] = len(candidates)
        ranked = evaluate_and_rank(candidates)
        if ranked:
            result["top_score"] = ranked[0].get("adjusted_score") if isinstance(ranked[0], dict) else None
        cand = candidates[0] if candidates else None
        if cand:
            val = validate_export(cand)
            result["guardrail_status"] = val.get("status")
            exp = export_musicxml(cand)
            result["export_ok"] = exp.get("error") is None
            result["export_error"] = exp.get("error")
            result["musicxml_len"] = len(exp.get("musicxml", ""))
    except Exception as e:
        result["error"] = str(e)
    return result


def main():
    prompts = [
        "floating chamber modern theme",
        "asymmetrical lyrical head",
        "modern big band opener",
        "lead sheet song about distance",
        "atmospheric nocturnal miniature",
    ]

    trials: List[Dict[str, Any]] = []

    # Single-engine presets (3+)
    single_presets = ["wheeler_lyric", "barry_bebop", "frisell_atmosphere", "shorter_head", "hill_modern", "monk_rhythm", "bartok_night", "scofield_holland", "big_band", "shorter_form", "ligeti_texture"]
    for preset in single_presets:
        n_prompts = 3 if preset in ["wheeler_lyric", "barry_bebop", "frisell_atmosphere"] else 1
        for i, prompt in enumerate(prompts[:n_prompts]):
            t = run_trial(preset, prompt, seed=10 + i)
            trials.append(t)
            print(f"  {preset} / {prompt[:30]}... -> {t.get('candidate_count', 0)} cand, score={t.get('top_score')}, export={t.get('export_ok')}")

    # Hybrid presets (3) - use pipeline presets
    hybrid_presets = ["hybrid_counterpoint", "chamber_jazz"]
    for preset in hybrid_presets:
        for i, prompt in enumerate(prompts[:2]):
            t = run_trial(preset, prompt, seed=20 + i)
            trials.append(t)
            print(f"  {preset} / {prompt[:30]}... -> {t.get('candidate_count', 0)} cand, score={t.get('top_score')}, export={t.get('export_ok')}")

    # Explicit hybrid (form + harmony + texture + orch)
    hybrid_roles = {
        "form_engine": "wayne_shorter",
        "harmony_engine": "wheeler_lyric",
        "texture_engine": "ligeti_texture",
        "orchestration_engine": "big_band",
    }
    t = run_hybrid_trial(hybrid_roles, "modern big band opener", seed=30)
    trials.append(t)
    print(f"  hybrid(big_band) / modern big band opener -> {t.get('candidate_count')} cand, score={t.get('top_score')}, export={t.get('export_ok')}")

    # Orchestration-oriented (2)
    orch_presets = ["guitar_string_quartet", "chamber_jazz"]
    for preset in orch_presets:
        t = run_trial(preset, "floating chamber modern theme", seed=40)
        trials.append(t)
        print(f"  {preset} / floating chamber... -> {t.get('candidate_count')} cand, export={t.get('export_ok')}")

    # Lead-sheet (2)
    lead_presets = ["lead_sheet_song", "wheeler_lyric"]  # wheeler for lead-sheet export test
    for preset in lead_presets:
        t = run_trial(preset, "lead sheet song about distance", seed=50)
        trials.append(t)
        print(f"  {preset} / lead sheet... -> {t.get('candidate_count')} cand, export={t.get('export_ok')}")

    # Summary by preset
    by_preset: Dict[str, List[Dict]] = {}
    for t in trials:
        p = t["preset"]
        if p not in by_preset:
            by_preset[p] = []
        by_preset[p].append(t)

    report = {
        "timestamp": datetime.now().isoformat(),
        "trials": trials,
        "by_preset": {p: [{"candidate_count": x["candidate_count"], "top_score": x["top_score"], "export_ok": x["export_ok"], "guardrail": x["guardrail_status"]} for x in v] for p, v in by_preset.items()},
    }

    out_dir = os.path.join(os.path.dirname(__file__), "docs", "trial_output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "preset_trial_results.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nResults saved to {out_path}")
    return report


if __name__ == "__main__":
    main()
