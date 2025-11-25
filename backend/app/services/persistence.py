from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import asyncio

_client = None
_db = None

def get_client():
    global _client, _db
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URI)
        _db = _client[settings.MONGO_DB]
    return _client, _db

async def save_message(doc: dict):
    _, db = get_client()
    await db.messages.insert_one(doc)

async def update_message_status(message_id: str, status: str):
    _, db = get_client()
    await db.messages.update_one({"message_id": message_id}, {"$set": {"status": status}})

async def list_messages(conversation_id: str, limit: int = 100):
    _, db = get_client()
    cursor = db.messages.find({"conversation_id": conversation_id}).sort("timestamp", 1).limit(limit)
    return [doc async for doc in cursor]
