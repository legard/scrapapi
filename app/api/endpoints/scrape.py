import logging

from fastapi import APIRouter

from app.models.schemas import ScrapeRequest, TaskResponse, TaskStatus
from app.services.scraper import scrape_url

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/scrape", response_model=TaskResponse)
async def create_scrape_task(request: ScrapeRequest):
    logger.info(f"Creating scrape task for URL: {request.url}")
    task = scrape_url.delay(str(request.url))
    logger.info(f"Scrape task created with ID: {task.id}")
    return TaskResponse(task_id=task.id, status=TaskStatus.PENDING)
