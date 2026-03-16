"""Final music export check — composition, hybrid, ensemble, lead-sheet."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    from backend.generation.pipeline import generate_candidates
    from backend.integration.hybrid_runtime_adapter import generate_hybrid
    from backend.integration.evaluation_service import evaluate_and_rank
    from backend.export.export_handler import export_musicxml, export_orchestrated_score, export_lead_sheet
    from backend.orchestration.orchestration_adapter import orchestrate_composition
    from backend.songwriting.songwriting_adapter import build_lead_sheet
    from backend.project.project_manager import create_project, create_run_folder

    out_dir = os.path.join(os.path.dirname(__file__), "docs", "trial_output", "exports")
    os.makedirs(out_dir, exist_ok=True)
    paths = {}

    # 1. Composition MusicXML (single-engine)
    gen = generate_candidates("wheeler_lyric", "floating chamber theme", 1)
    ranked = gen.get("ranked", [])
    cand = ranked[0] if ranked else gen.get("candidates", [{}])[0]
    if hasattr(cand, "compiled_result"):
        cand = cand.compiled_result if isinstance(cand.compiled_result, dict) else cand
    comp = cand.get("compiled") if isinstance(cand, dict) else None
    if comp:
        exp = export_musicxml(cand)
        p1 = os.path.join(out_dir, "composition_wheeler.musicxml")
        if exp.get("musicxml"):
            with open(p1, "w") as f:
                f.write(exp["musicxml"])
            paths["composition"] = p1

    # 2. Hybrid MusicXML
    h = generate_hybrid(
        {"form_engine": "wayne_shorter", "harmony_engine": "wheeler_lyric", "texture_engine": "ligeti_texture"},
        {"input_text": "Test", "seed": 0, "count": 1},
    )
    if h:
        exp = export_musicxml(h[0])
        p2 = os.path.join(out_dir, "hybrid.musicxml")
        if exp.get("musicxml"):
            with open(p2, "w") as f:
                f.write(exp["musicxml"])
            paths["hybrid"] = p2

    # 3. Ensemble MusicXML
    if comp:
        orch = orchestrate_composition(comp, "guitar_string_quartet", 0)
        ens = export_orchestrated_score(orch.get("ensemble_arrangement"))
        p3 = os.path.join(out_dir, "ensemble_quartet.musicxml")
        if ens.get("musicxml"):
            with open(p3, "w") as f:
                f.write(ens["musicxml"])
            paths["ensemble"] = p3

    # 4. Lead-sheet MusicXML
    if comp:
        ls = build_lead_sheet(comp)
        ls_exp = export_lead_sheet(ls.get("lead_sheet"))
        p4 = os.path.join(out_dir, "lead_sheet.musicxml")
        if ls_exp.get("musicxml"):
            with open(p4, "w") as f:
                f.write(ls_exp["musicxml"])
            paths["lead_sheet"] = p4

    for k, v in paths.items():
        print(f"{k}: {v}")
    return paths

if __name__ == "__main__":
    main()
