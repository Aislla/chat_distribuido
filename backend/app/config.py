import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "chat4all")
    KAFKA_BOOTSTRAP: str = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "messages")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))

settings = Settings()
