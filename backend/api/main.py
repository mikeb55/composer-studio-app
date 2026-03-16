"""
Composer Studio Backend API — FastAPI service.
"""

import os
import sys

# Add creative-engines/engines to path (sibling repo)
_ce = os.environ.get("CREATIVE_ENGINES_PATH")
if _ce:
    _eng = os.path.join(_ce, "engines") if os.path.isdir(os.path.join(_ce, "engines")) else _ce
    sys.path.insert(0, _eng)
else:
    _parent = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _ce_root = os.path.join(_parent, "creative-engines")
    _eng = os.path.join(_ce_root, "engines")
    if os.path.isdir(_eng):
        sys.path.insert(0, _eng)
    else:
        _ce_root = os.path.abspath(os.path.join(_parent, "..", "creative-engines"))
        _eng = os.path.join(_ce_root, "engines")
        if os.path.isdir(_eng):
            sys.path.insert(0, _eng)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import generate, rank, orchestrate, songwriting, export_routes, project, engines

app = FastAPI(title="Composer Studio API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router, prefix="/generate", tags=["generate"])
app.include_router(rank.router, prefix="/rank", tags=["rank"])
app.include_router(orchestrate.router, prefix="/orchestrate", tags=["orchestrate"])
app.include_router(songwriting.router, prefix="/create_leadsheet", tags=["songwriting"])
app.include_router(export_routes.router, prefix="/export", tags=["export"])
app.include_router(project.router, prefix="/project", tags=["project"])
app.include_router(engines.router, prefix="/engines", tags=["engines"])


@app.get("/")
def root():
    return {"status": "ok", "service": "Composer Studio API"}
