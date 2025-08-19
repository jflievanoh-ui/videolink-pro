import os
from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import socketio

app = FastAPI()

# Permite todas las orígenes (en producción restringe a tu dominio)
origins = [
    "https://videolink-frontend.onrender.com",
    # Añade más si lo necesitas
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket endpoint
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Tu lógica de señalización aquí

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
