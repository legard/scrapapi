import logging

from fastapi import APIRouter

from app.api.endpoints import scrape, tasks

logger = logging.getLogger(__name__)

api_router = APIRouter()
api_router.include_router(scrape.router, tags=["scrape"])
api_router.include_router(tasks.router, tags=["tasks"])

logger.info("API routes initialized")



