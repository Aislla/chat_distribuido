import asyncio
import json
from aiokafka import AIOKafkaConsumer
from ..services.persistence import update_message_status, save_message
from ..config import settings
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("router_worker")

async def run_worker():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP,
        group_id="router-worker-group",
        enable_auto_commit=True
    )
    await consumer.start()
    try:
        async for msg in consumer:
            try:
                payload = json.loads(msg.value.decode())
                message_id = payload["message_id"]
                logger.info(f"Worker consumed message_id={message_id} conversation={payload.get('conversation_id')}")
                # Simulate delivery processing
                await update_message_status(message_id, "DELIVERED")
                logger.info(f"Updated message {message_id} status -> DELIVERED")
                # Optionally: emit audit log or webhook
            except Exception as e:
                logger.exception("Error processing message: %s", e)
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(run_worker())
