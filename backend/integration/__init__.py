"""
Creative-engines integration — Registry-based engine loading and generation.
"""

from backend.integration.engine_repo_config import ENGINE_REPO_PATH
from backend.integration.engine_registry_loader import (
    ensure_engines_loaded,
    get_engine,
    list_engines,
)
from backend.integration.engine_runtime_adapter import generate, export_musicxml, get_musicxml_path
from backend.integration.hybrid_runtime_adapter import (
    generate_hybrid_candidates,
    generate_hybrid_candidate,
)
from backend.integration.generation_service import (
    create_candidates,
    create_single_engine_candidates,
    create_hybrid_candidates,
    list_available_engines,
    list_presets,
)
from backend.integration.evaluation_service import (
    evaluate_and_rank,
    rank_candidates,
)

__all__ = [
    "ENGINE_REPO_PATH",
    "ensure_engines_loaded",
    "get_engine",
    "list_engines",
    "generate",
    "export_musicxml",
    "get_musicxml_path",
    "generate_hybrid_candidates",
    "generate_hybrid_candidate",
    "create_candidates",
    "create_single_engine_candidates",
    "create_hybrid_candidates",
    "list_available_engines",
    "list_presets",
    "evaluate_and_rank",
    "rank_candidates",
]
