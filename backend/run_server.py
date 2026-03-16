"""
Run Composer Studio Backend API.
"""

import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host="127.0.0.1",
        port=8765,
        reload=True,
    )
