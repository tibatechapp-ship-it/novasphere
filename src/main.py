"""NovaSphere application entrypoint."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .ws_manager import ConnectionManager

BASE_DIR = Path(__file__).resolve().parent.parent
manager = ConnectionManager()

app = FastAPI(title="NovaSphere", version="0.1.0")

static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir), html=False), name="static")


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    template = BASE_DIR / "templates" / "index.html"
    return template.read_text(encoding="utf-8")


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": "novasphere",
        "version": "0.1.0",
        "connections": manager.count,
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    await manager.broadcast(f"[system] a new node connected ({manager.count} online)")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"[broadcast] {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"[system] a node disconnected ({manager.count} online)")
