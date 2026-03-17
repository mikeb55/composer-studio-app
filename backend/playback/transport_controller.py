"""
Transport controller — Play / Stop / Pause / Loop state.
"""

from enum import Enum
from typing import Optional


class TransportState(str, Enum):
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


class TransportController:
    """Manages playback state. Actual audio is delegated to playback_service."""

    def __init__(self):
        self._state = TransportState.STOPPED
        self._current_file: Optional[str] = None
        self._loop_start: Optional[int] = None
        self._loop_end: Optional[int] = None

    @property
    def state(self) -> TransportState:
        return self._state

    @property
    def current_file(self) -> Optional[str]:
        return self._current_file

    @property
    def loop_start(self) -> Optional[int]:
        return self._loop_start

    @property
    def loop_end(self) -> Optional[int]:
        return self._loop_end

    def load(self, file_path: str, loop_start: Optional[int] = None, loop_end: Optional[int] = None) -> None:
        self._current_file = file_path
        self._loop_start = loop_start
        self._loop_end = loop_end

    def play(self) -> None:
        self._state = TransportState.PLAYING

    def stop(self) -> None:
        self._state = TransportState.STOPPED

    def pause(self) -> None:
        self._state = TransportState.PAUSED

    def set_loop(self, start: Optional[int], end: Optional[int]) -> None:
        self._loop_start = start
        self._loop_end = end

    def status(self) -> dict:
        return {
            "state": self._state.value,
            "current_file": self._current_file,
            "loop_start": self._loop_start,
            "loop_end": self._loop_end,
        }
