import json
from collections import defaultdict

class SocketManager:
    """
    Keeps track of connected clients and room membership.
    Handles forwarding of SDP & ICE messages between peers.
    """

    def __init__(self):
        # room_id -> set(sid)
        self.rooms = defaultdict(set)

    async def on_connect(self, sid: str, environ):
        print(f"[SOCKET] Connected {sid}")

    async def on_disconnect(self, sid: str):
        for room_id, members in list(self.rooms.items()):
            if sid in members:
                members.remove(sid)
                if not members:  # limpiar si la sala queda vacía
                    del self.rooms[room_id]
        print(f"[SOCKET] Disconnected {sid}")

    async def join_room(self, sid: str, room_id: str):
        from app.main import sio  # import local para evitar circular imports
        self.rooms[room_id].add(sid)
        print(f"[SOCKET] {sid} joined room {room_id}")
        await sio.emit("joined", {"room": room_id, "sid": sid}, to=sid)

    async def forward_to_peer(self, event_type: str, data: dict):
        """
        `data` must contain:
          - room_id: str
          - target: recipient's socket id
          - payload: SDP or ICE object
        """
        from app.main import sio  # import local para evitar circular imports
        room_id = data.get("room_id")
        target_sid = data.get("target")
        payload = data.get("payload")

        if not room_id or not target_sid or not payload:
            print(f"[SOCKET] Invalid forward data: {data}")
            return

        if target_sid in self.rooms.get(room_id, []):
            await sio.emit(event_type, payload, to=target_sid)
            print(f"[SOCKET] Forwarded {event_type} to {target_sid} in room {room_id}")
        else:
            print(f"[SOCKET] Target {target_sid} not in room {room_id}")

# Global instance
sio_manager = SocketManager()
