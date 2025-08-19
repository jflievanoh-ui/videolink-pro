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
        for room in list(self.rooms.values()):
            if sid in room:
                room.remove(sid)
        print(f"[SOCKET] Disconnected {sid}")

    async def join_room(self, sid: str, room_id: str):
        self.rooms[room_id].add(sid)
        await sio.emit('joined', {"room": room_id}, to=sid)

    async def forward_to_peer(self, event_type: str, data: dict):
        """
        `data` must contain:
          - sid: recipient's socket id
          - payload: SDP or ICE object
        """
        target_sid = data['sid']
        await sio.emit(event_type, data['payload'], to=target_sid)

sio_manager = SocketManager()
