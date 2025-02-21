import logging

from celery import Celery  # type: ignore[attr-defined]

from app.core.config import settings

logger = logging.getLogger(__name__)

celery_app = Celery(
    "worker",
    broker=f"{settings.REDIS_URL}/0",
    backend=f"{settings.REDIS_URL}/1",
    include=["app.services.scraper"],
)

celery_app.conf.task_routes = {"app.services.scraper.*": {"queue": "main-queue"}}

logger.info("Celery application initialized")
