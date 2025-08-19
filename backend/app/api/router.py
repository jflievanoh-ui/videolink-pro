from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
import motor.motor_asyncio

from app.db.client import get_db
from app.auth.jwt import create_access_token

router = APIRouter()

class RoomCreate(BaseModel):
    name: str = Field(..., max_length=50)

class RoomOut(BaseModel):
    id: str
    name: str
    created_at: str

@router.post("/rooms", response_model=RoomOut)
async def create_room(payload: RoomCreate):
    db = get_db()
    room_doc = {
        "name": payload.name,
        "created_at": datetime.utcnow(),
    }
    result = await db.rooms.insert_one(room_doc)
    room_doc["_id"] = result.inserted_id
    return RoomOut(
        id=str(result.inserted_id),
        name=payload.name,
        created_at=room_doc["created_at"].isoformat()
    )

@router.get("/rooms/{room_id}", response_model=RoomOut)
async def get_room(room_id: str):
    db = get_db()
    room = await db.rooms.find_one({"_id": ObjectId(room_id)})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return RoomOut(
        id=str(room["_id"]),
        name=room["name"],
        created_at=room["created_at"].isoformat()
    )
