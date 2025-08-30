from fastapi import FastAPI

from app.api.api import api_router
from app.core.config import settings

app = FastAPI(title="hatch-messaging-service", debug=settings.debug)

app.include_router(api_router, prefix="/api")
