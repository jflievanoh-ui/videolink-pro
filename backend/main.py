import os
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.db.client import get_db
from app.api.router import api_router   # <--- ahora sí api_router
from app.sockets.manager import sio_manager

# ---- Configuración FastAPI ----
app = FastAPI()

# CORS (ajusta dominios en producción)
origins = [
    "https://videolink-frontend.onrender.com",
    "http://localhost:3000",  # opcional para pruebas locales
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- WebSocket nativo (pruebas directas) ----
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Aquí va tu lógica de señalización o pruebas
        await websocket.send_text(f"Echo desde room {room_id}: {data}")

# ---- Socket.IO ----
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=origins
)
asgi_app = socketio.ASGIApp(sio, other_asgi_app=app)

# ---- REST API ----
app.include_router(api_router, prefix="/api")   # <--- incluye tus endpoints

# ---- Eventos Socket.IO ----
@sio.event
async def connect(sid, environ):
    await sio_manager.on_connect(sid, environ)

@sio.event
async def disconnect(sid):
    await sio_manager.on_disconnect(sid)

@sio.event
async def join_room(sid, data):
    await sio_manager.join_room(sid, data["room_id"])

@sio.event
async def offer(sid, data):
    await sio_manager.forward_to_peer("offer", data)

@sio.event
async def answer(sid, data):
    await sio_manager.forward_to_peer("answer", data)

@sio.event
async def ice_candidate(sid, data):
    await sio_manager.forward_to_peer("ice-candidate", data)

# ---- Healthcheck ----
@app.get("/health")
async def health():
    return {"status": "ok"}
