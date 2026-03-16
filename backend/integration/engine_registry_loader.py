"""
Engine registry loader — Load engines through the creative-engines registry only.

Do NOT import engine modules directly. Always use the registry.
Flow: load engine registry → request engine by name → call generation methods via registry.
"""

import os
import sys
from typing import Any, List

from backend.integration.engine_repo_config import ENGINE_REPO_PATH

_CE_PATH_ADDED = False


def _ensure_ce_path() -> None:
    """Add creative-engines engines dir to sys.path so registry can be imported."""
    global _CE_PATH_ADDED
    if _CE_PATH_ADDED:
        return
    engines_dir = os.path.join(ENGINE_REPO_PATH, "engines")
    if os.path.isdir(engines_dir) and engines_dir not in sys.path:
        sys.path.insert(0, engines_dir)
        _CE_PATH_ADDED = True


def ensure_engines_loaded() -> None:
    """Ensure built-in engines are registered. Call before list_engines/get_engine."""
    _ensure_ce_path()
    from shared_composer.engine_registry import ensure_engines_loaded as _ensure
    _ensure()


def list_engines() -> List[str]:
    """List all registered engine names."""
    ensure_engines_loaded()
    from shared_composer.engine_registry import list_engines as _list
    return _list()


def get_engine(engine_name: str) -> Any:
    """Get engine instance by name via registry. Returns new instance each call."""
    ensure_engines_loaded()
    from shared_composer.engine_registry import get_engine as _get
    return _get(engine_name)
