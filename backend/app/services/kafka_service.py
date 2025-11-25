import asyncio
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from .config import settings

producer = None

async def get_producer(loop):
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP)
        await producer.start()
    return producer

async def send_message_event(loop, message: dict):
    p = await get_producer(loop)
    # partitioning by conversation_id via key
    key = message.get("conversation_id", "").encode()
    await p.send_and_wait(settings.KAFKA_TOPIC, json.dumps(message).encode(), key=key)
