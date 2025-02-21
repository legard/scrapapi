from celery.result import AsyncResult
from fastapi import APIRouter

from app.core.celery import celery_app
from app.models.schemas import ScrapedData, TaskResponse, TaskStatus

router = APIRouter()


@router.get("/task/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    task: AsyncResult = AsyncResult(task_id, app=celery_app)

    if task.failed():
        return TaskResponse(
            task_id=task_id, status=TaskStatus.FAILURE, error=str(task.result)
        )

    if task.ready():
        result = task.get()
        return TaskResponse(
            task_id=task_id, status=TaskStatus.SUCCESS, result=ScrapedData(**result)
        )

    return TaskResponse(
        task_id=task_id,
        status=TaskStatus.PROCESSING if task.state == "STARTED" else TaskStatus.PENDING,
    )
