"""End-to-end verification script - uses backend integration directly."""
import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    results = {}
    
    # Step 2: Engine discovery
    from backend.integration.engine_registry_loader import list_engines
    engines = list_engines()
    results["engines"] = {"total": len(engines), "names": engines}
    
    # Step 4: Hybrid generation - use wayne_shorter for reliable guardrail pass
    # (shorter_form has melody_blueprint structure that can vary)
    from backend.integration.hybrid_runtime_adapter import generate_hybrid
    from backend.integration.evaluation_service import evaluate_and_rank
    from backend.validation.export_guard import validate_export
    from backend.export.export_handler import export_musicxml
    
    engine_roles = {
        "form_engine": "wayne_shorter",
        "harmony_engine": "wheeler_lyric",
        "texture_engine": "ligeti_texture",
        "orchestration_engine": "big_band",
    }
    h_candidates = generate_hybrid(engine_roles, {"input_text": "Test", "seed": 0, "count": 1})
    h_ranked = evaluate_and_rank(h_candidates)
    h_top = h_ranked[0] if h_ranked else {}
    h_cand = h_candidates[0] if h_candidates else {}
    
    val = validate_export(h_cand)
    exp = export_musicxml(h_cand)
    
    results["hybrid"] = {
        "score": h_top.get("adjusted_score") if isinstance(h_top, dict) else None,
        "guardrail_status": val.get("status"),
        "musicxml_len": len(exp.get("musicxml", "")),
        "export_blocked": exp.get("error"),
    }
    
    # Step 3: Single-engine generation
    from backend.generation.pipeline import generate_candidates
    gen = generate_candidates("wheeler_lyric", "floating chamber theme", 1)
    candidates = gen.get("candidates", [])
    ranked = gen.get("ranked", [])
    top = ranked[0] if ranked else {}
    cand_for_export = candidates[0] if candidates else {}
    if ranked:
        cr = getattr(top, "compiled_result", top) if hasattr(top, "compiled_result") else top
        cand_for_export = cr if isinstance(cr, dict) else cand_for_export
    
    from backend.export.export_handler import export_musicxml
    export_res = export_musicxml(cand_for_export)
    musicxml = export_res.get("musicxml", "")
    results["single"] = {
        "candidate_count": len(candidates),
        "top_score": getattr(top, "adjusted_score", top.get("adjusted_score") if isinstance(top, dict) else None),
        "musicxml_len": len(musicxml),
        "export_error": export_res.get("error"),
    }
    
    # Step 5: Project system
    from backend.project.project_manager import create_project, create_run_folder, save_run_metadata, list_projects
    
    proj = create_project("verification_project")
    proj_path = proj.get("path", "")
    
    run1 = create_run_folder("verification_project", "single_run")
    run_path1 = run1.get("run_path", "")
    save_run_metadata(run_path1, "wheeler_lyric", "floating chamber theme", 1)
    
    run2 = create_run_folder("verification_project", "hybrid_run")
    save_run_metadata(run2.get("run_path", ""), "hybrid", "Test", 0)
    
    projects = list_projects()
    results["project"] = {
        "project_path": proj_path,
        "run_count": 2,
        "projects": projects,
    }
    
    # Step 6: Orchestration + Lead sheet
    comp = cand_for_export.get("compiled") if isinstance(cand_for_export, dict) else None
    if comp:
        try:
            from backend.orchestration.orchestration_adapter import orchestrate_composition
            orch = orchestrate_composition(comp, "guitar_string_quartet", 0)
            from backend.export.export_handler import export_orchestrated_score
            ens_exp = export_orchestrated_score(orch.get("ensemble_arrangement"))
            results["orchestration"] = {"musicxml_len": len(ens_exp.get("musicxml", "")), "error": ens_exp.get("error")}
        except Exception as e:
            results["orchestration"] = {"error": str(e)}
        
        try:
            from backend.songwriting.songwriting_adapter import build_lead_sheet
            ls = build_lead_sheet(comp)
            from backend.export.export_handler import export_lead_sheet
            ls_exp = export_lead_sheet(ls.get("lead_sheet"))
            results["lead_sheet"] = {"musicxml_len": len(ls_exp.get("musicxml", "")), "error": ls_exp.get("error")}
        except Exception as e:
            results["lead_sheet"] = {"error": str(e)}
    else:
        results["orchestration"] = {"error": "No compiled"}
        results["lead_sheet"] = {"error": "No compiled"}
    
    print(json.dumps(results, indent=2))
    
    # Output tree (projects at parent of composer-studio-app)
    proj_dir = os.path.dirname(proj_path) if proj_path else ""
    if os.path.isdir(proj_dir):
        print("\n--- Output tree (projects/) ---")
        for root, dirs, files in os.walk(proj_dir):
            level = root.replace(proj_dir, "").count(os.sep)
            indent = "  " * level
            print(f"{indent}{os.path.basename(root) or 'projects'}/")
            for f in sorted(files)[:5]:
                print(f"{indent}  {f}")
            if len(files) > 5:
                print(f"{indent}  ... ({len(files)} more)")

if __name__ == "__main__":
    main()
