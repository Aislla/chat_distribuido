from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid, time
from ..services.auth import verify_jwt
from ..services.kafka_service import send_message_event
from ..services.persistence import list_messages, save_message
from ..config import settings
import asyncio

router = APIRouter(prefix="/v1")

class Payload(BaseModel):
    type: str = "text"
    text: Optional[str] = None
    file_url: Optional[str] = None

class SendMessageRequest(BaseModel):
    conversation_id: str
    to: List[str]
    channels: List[str] = Field(default_factory=lambda: ["internal"])
    payload: Payload

class MessageResponse(BaseModel):
    message_id: str
    conversation_id: str
    from_user: str
    to: List[str]
    channels: List[str]
    payload: Payload
    status: str
    timestamp: float

@router.post("/messages", response_model=MessageResponse)
async def post_message(req: SendMessageRequest, token=Depends(verify_jwt)):
    # token expected to contain "user_id"
    user_id = token.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    message_id = str(uuid.uuid4())
    timestamp = time.time()
    doc = {
        "message_id": message_id,
        "conversation_id": req.conversation_id,
        "from": user_id,
        "to": req.to,
        "channels": req.channels,
        "payload": req.payload.dict(),
        "status": "SENT",
        "timestamp": timestamp
    }
    # Persist initial SENT state (optional: worker will also persist)
    await save_message(doc)
    # Enqueue event in Kafka
    loop = asyncio.get_event_loop()
    await send_message_event(loop, doc)
    return {
        "message_id": message_id,
        "conversation_id": req.conversation_id,
        "from_user": user_id,
        "to": req.to,
        "channels": req.channels,
        "payload": req.payload,
        "status": "SENT",
        "timestamp": timestamp
    }

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(conversation_id: str, token=Depends(verify_jwt)):
    docs = await list_messages(conversation_id)
    # map to response model
    out = []
    for d in docs:
        out.append({
            "message_id": d["message_id"],
            "conversation_id": d["conversation_id"],
            "from_user": d["from"],
            "to": d.get("to", []),
            "channels": d.get("channels", []),
            "payload": d.get("payload", {}),
            "status": d.get("status", "SENT"),
            "timestamp": d.get("timestamp")
        })
    return out
