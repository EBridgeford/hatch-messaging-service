from fastapi import APIRouter

from app.api.endpoints import conversations, messages, webhooks

api_router = APIRouter()
api_router.include_router(
    conversations.router, prefix="/conversations", tags=["conversations"]
)
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["messages"])
