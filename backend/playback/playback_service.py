"""
Playback service — Orchestrates MIDI render and transport for candidate audition.
"""

import os
import uuid
from typing import Any, Dict, Optional

from backend.playback.midi_renderer import musicxml_to_midi
from backend.playback.transport_controller import TransportController, TransportState


# Singleton transport
_transport = TransportController()

# Resolved paths for playback (outputs dir)
_outputs_dir: Optional[str] = None


def _get_outputs_dir() -> str:
    global _outputs_dir
    if _outputs_dir is None:
        _here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        _outputs_dir = os.path.join(_here, "outputs")
        os.makedirs(_outputs_dir, exist_ok=True)
    return _outputs_dir


def _resolve_path(file_path: str) -> Optional[str]:
    """Resolve file path. Accepts relative path under outputs/ or absolute."""
    if os.path.isabs(file_path) and os.path.isfile(file_path):
        return file_path
    base = _get_outputs_dir()
    # Normalize: strip leading / and outputs/ prefix
    normalized = file_path.replace("\\", "/").lstrip("/")
    if normalized.lower().startswith("outputs/"):
        normalized = normalized[8:]
    full = os.path.join(base, normalized)
    if os.path.isfile(full):
        return full
    # Try under project root
    _root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    full2 = os.path.join(_root, normalized)
    if os.path.isfile(full2):
        return full2
    return None


def _write_musicxml_temp(musicxml: str) -> Optional[str]:
    """Write MusicXML string to temp file in outputs/, return path."""
    base = _get_outputs_dir()
    name = f"playback_{uuid.uuid4().hex[:12]}.musicxml"
    path = os.path.join(base, name)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(musicxml)
        return path
    except OSError:
        return None


def play(
    file_path: Optional[str] = None,
    musicxml: Optional[str] = None,
    loop_start: Optional[int] = None,
    loop_end: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Start playback. Accepts file_path or musicxml string.
    Returns status JSON. Does not fake success.
    """
    path: Optional[str] = None
    if file_path:
        path = _resolve_path(file_path)
    elif musicxml:
        path = _write_musicxml_temp(musicxml)

    if not path or not os.path.isfile(path):
        return {
            "status": "error",
            "message": "No valid MusicXML file or content provided",
            "state": _transport.state.value,
        }

    ok, msg = musicxml_to_midi(path)
    if not ok:
        return {
            "status": "playback_not_implemented",
            "message": msg,
            "state": _transport.state.value,
            "file_path": path,
        }

    _transport.load(path, loop_start, loop_end)
    _transport.play()
    # TODO: Actually start MIDI playback (e.g. via pygame.midi, mido, or subprocess)
    return {
        "status": "playing",
        "state": _transport.state.value,
        "file_path": path,
        "loop_start": loop_start,
        "loop_end": loop_end,
    }


def stop() -> Dict[str, Any]:
    """Stop playback."""
    _transport.stop()
    # TODO: Stop actual audio
    return {
        "status": "stopped",
        "state": _transport.state.value,
    }


def pause() -> Dict[str, Any]:
    """Pause playback."""
    _transport.pause()
    # TODO: Pause actual audio
    return {
        "status": "paused",
        "state": _transport.state.value,
    }


def set_loop(loop_start: Optional[int], loop_end: Optional[int]) -> Dict[str, Any]:
    """Set loop region (measure numbers)."""
    _transport.set_loop(loop_start, loop_end)
    return {
        "status": "ok",
        "loop_start": loop_start,
        "loop_end": loop_end,
        "state": _transport.state.value,
    }


def status() -> Dict[str, Any]:
    """Get current playback status."""
    return {
        "status": "ok",
        **(_transport.status()),
    }
