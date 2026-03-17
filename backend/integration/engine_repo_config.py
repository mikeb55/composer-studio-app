"""
Engine repo config — Local path to creative-engines repository.
Uses relative path from this repo. Set CREATIVE_ENGINES_PATH env var to override.
"""

import os

# Relative from composer-studio-app root: ../creative-engines
_here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DEFAULT = os.path.normpath(os.path.join(_here, "..", "creative-engines"))
ENGINE_REPO_PATH = os.environ.get("CREATIVE_ENGINES_PATH") or _DEFAULT
