"""WebSocket connection manager for broadcasting messages to all clients."""

from __future__ import annotations

from fastapi import WebSocket


class ConnectionManager:
    """Tracks active WebSocket connections and broadcasts messages."""

    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:  # noqa: BLE001
                self.disconnect(connection)

    @property
    def count(self) -> int:
        return len(self.active_connections)
