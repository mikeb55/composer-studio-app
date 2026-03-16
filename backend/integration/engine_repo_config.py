"""
Engine repo config — Local path to creative-engines repository.
Set CREATIVE_ENGINES_PATH env var to override (e.g. for packaging).
"""

import os

_DEFAULT = r"C:\Users\mike\Documents\Cursor AI Projects\creative-engines"
ENGINE_REPO_PATH = os.environ.get("CREATIVE_ENGINES_PATH") or _DEFAULT
