import os
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.db.client import get_db
from app.api.router import api_router
from app.sockets.manager import sio_manager

# ---- Configuración FastAPI ----
app = FastAPI(title="Videolink Backend")

# ---- CORS ----
origins = [
    "https://videolink-frontend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- WebSocket nativo solo para pruebas locales ----
if os.environ.get("ENV", "prod") != "prod":
    @app.websocket("/ws-test/{room_id}")
    async def websocket_endpoint(websocket: WebSocket, room_id: str):
        await websocket.accept()
        while True:
            try:
                data = await websocket.receive_text()
                await websocket.send_text(f"Echo desde room {room_id}: {data}")
            except Exception as e:
                print(f"[WS ERROR] {e}")
                break

# ---- Socket.IO con WSS ----
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=origins
)
asgi_app = socketio.ASGIApp(sio, other_asgi_app=app)

# ---- REST API ----
app.include_router(api_router, prefix="/api")

# ---- Eventos Socket.IO ----
@sio.event
async def connect(sid, environ):
    print(f"[SOCKET.IO] Cliente conectado: {sid}")
    await sio_manager.on_connect(sid, environ)

@sio.event
async def disconnect(sid):
    print(f"[SOCKET.IO] Cliente desconectado: {sid}")
    await sio_manager.on_disconnect(sid)

@sio.event
async def join_room(sid, data):
    try:
        await sio_manager.join_room(sid, data["room_id"])
    except Exception as e:
        await sio.emit("error", {"msg": str(e)}, to=sid)

@sio.event
async def offer(sid, data):
    try:
        await sio_manager.forward_to_peer("offer", data)
    except Exception as e:
        await sio.emit("error", {"msg": str(e)}, to=sid)

@sio.event
async def answer(sid, data):
    try:
        await sio_manager.forward_to_peer("answer", data)
    except Exception as e:
        await sio.emit("error", {"msg": str(e)}, to=sid)

@sio.event
async def ice_candidate(sid, data):
    try:
        await sio_manager.forward_to_peer("ice-candidate", data)
    except Exception as e:
        await sio.emit("error", {"msg": str(e)}, to=sid)

# ---- Healthcheck ----
@app.get("/health")
async def health():
    return {"status": "ok"}

# ---- Run Uvicorn (Render asigna $PORT) ----
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:asgi_app", host="0.0.0.0", port=port)
