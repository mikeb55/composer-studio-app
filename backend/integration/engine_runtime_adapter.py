"""
Engine runtime adapter — Clean wrapper for single-engine generation.

Loads engine via registry, executes generation, returns candidate results,
exports MusicXML paths.
"""

import os
from typing import Any, Dict, Optional

from backend.integration.engine_registry_loader import get_engine, ensure_engines_loaded


def generate(
    engine_name: str,
    input_text: str,
    seed: int = 0,
    mode: str = "title",
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Load engine via registry, generate IR, compile, return candidate dict.
    """
    ensure_engines_loaded()
    eng = get_engine(engine_name)
    ir = eng.generate_ir(input_text, mode=mode, seed=seed, **kwargs)
    compiled = eng.compile_from_ir(ir)
    return {
        "compiled": compiled,
        "melody_engine": engine_name,
        "harmony_engine": engine_name,
        "hybrid_ir": None,
    }


def export_musicxml(candidate: Dict[str, Any], output_dir: Optional[str] = None) -> str:
    """
    Export candidate to MusicXML string and optionally write to file.
    Returns path to saved file if output_dir given, else returns MusicXML string.
    For single-engine: uses engine's export_musicxml.
    """
    ensure_engines_loaded()
    compiled = candidate.get("compiled")
    if not compiled:
        return ""
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    engine_name = candidate.get("melody_engine", "wayne_shorter")
    eng = get_engine(engine_name)
    xml_str = eng.export_musicxml(compiled)
    if output_dir:
        path = os.path.join(output_dir, "composition.musicxml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml_str)
        return path
    return xml_str


def get_musicxml_path(candidate: Dict[str, Any], output_dir: str) -> str:
    """
    Export candidate to MusicXML file and return path.
    """
    return export_musicxml(candidate, output_dir)
