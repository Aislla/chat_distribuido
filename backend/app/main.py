from fastapi import FastAPI
from .routes.messages import router as messages_router
from .config import settings

app = FastAPI(title="Chat4All API", version="0.1")

app.include_router(messages_router)

@app.get("/")
async def root():
    return {"service": "chat4all-api", "version": "0.1"}
