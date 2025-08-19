import os
from fastapi import FastAPI, Request, WebSocket
import socketio

from app.db.client import get_db
from app.api.router import api_router
from app.sockets.manager import sio_manager

# ---- ASGI App ----
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
app = FastAPI()
sio.attach(app)

# Mount REST API routes
app.include_router(api_router, prefix="/api")

# Socket.io event handlers
@sio.event
async def connect(sid: str, environ):
    await sio_manager.on_connect(sid, environ)

@sio.event
async def disconnect(sid: str):
    await sio_manager.on_disconnect(sid)

@sio.event
async def join_room(data):
    await sio_manager.join_room(data['sid'], data['room_id'])

@sio.event
async def offer(data):
    await sio_manager.forward_to_peer('offer', data)

@sio.event
async def answer(data):
    await sio_manager.forward_to_peer('answer', data)

@sio.event
async def ice_candidate(data):
    await sio_manager.forward_to_peer('ice-candidate', data)

# Optional: expose health endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}
