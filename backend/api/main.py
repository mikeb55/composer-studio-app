"""
Composer Studio Backend API — FastAPI service.
"""

import os
import sys

# Add creative-engines/engines to path (uses relative path from engine_repo_config)
from backend.integration.engine_repo_config import ENGINE_REPO_PATH
_eng = os.path.join(ENGINE_REPO_PATH, "engines")
if os.path.isdir(_eng) and _eng not in sys.path:
    sys.path.insert(0, _eng)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.routes import generate, rank, orchestrate, songwriting, export_routes, project, engines, hybrid, validation, playback

app = FastAPI(title="Composer Studio API", version="0.1.0")

# Serve MusicXML outputs (e.g. /outputs/foo.musicxml)
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_outputs = os.path.join(_root, "outputs")
_projects = os.path.join(_root, "projects")
os.makedirs(_outputs, exist_ok=True)
os.makedirs(_projects, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=_outputs), name="outputs")
app.mount("/projects", StaticFiles(directory=_projects), name="projects")
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
app.include_router(hybrid.router, prefix="/hybrid", tags=["hybrid"])
app.include_router(validation.router, prefix="/validation", tags=["validation"])
app.include_router(playback.router, prefix="/playback", tags=["playback"])


@app.get("/")
def root():
    return {"status": "ok", "service": "Composer Studio API"}
