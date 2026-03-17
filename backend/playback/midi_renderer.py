"""
MIDI renderer — Convert MusicXML to MIDI for playback.

TODO: Implement full MusicXML→MIDI conversion.
Options: music21, musicxml2midi, or external tool.
For now returns structured placeholder status.
"""

import os
from typing import Optional, Tuple


def musicxml_to_midi(musicxml_path: str, output_path: Optional[str] = None) -> Tuple[bool, str]:
    """
    Convert MusicXML file to MIDI.

    Returns:
        (success, message_or_midi_path)
    """
    if not os.path.isfile(musicxml_path):
        return False, f"File not found: {musicxml_path}"

    # TODO: Implement actual conversion.
    # Example with music21:
    #   from music21 import converter
    #   score = converter.parse(musicxml_path)
    #   score.write('midi', fp=output_path)
    return False, "MusicXML→MIDI conversion not yet implemented"


def get_measure_count(musicxml_path: str) -> int:
    """
    Parse MusicXML to get measure count (for loop bounds).
    Returns 0 if unparseable.
    """
    if not os.path.isfile(musicxml_path):
        return 0
    # TODO: Parse MusicXML to count measures (e.g. via music21 or xml.etree)
    return 0
