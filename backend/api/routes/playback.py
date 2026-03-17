"""Playback endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from backend.playback.playback_service import play, stop, pause, set_loop, status

router = APIRouter()


class PlayRequest(BaseModel):
    file_path: Optional[str] = None
    musicxml: Optional[str] = None
    loop_start: Optional[int] = None
    loop_end: Optional[int] = None


class LoopRequest(BaseModel):
    loop_start: Optional[int] = None
    loop_end: Optional[int] = None


@router.post("/play")
def play_endpoint(req: PlayRequest):
    return play(
        file_path=req.file_path,
        musicxml=req.musicxml,
        loop_start=req.loop_start,
        loop_end=req.loop_end,
    )


@router.post("/stop")
def stop_endpoint():
    return stop()


@router.post("/pause")
def pause_endpoint():
    return pause()


@router.post("/loop")
def loop_endpoint(req: LoopRequest):
    return set_loop(req.loop_start, req.loop_end)


@router.get("/status")
def status_endpoint():
    return status()
