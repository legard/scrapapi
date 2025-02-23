from datetime import datetime
from enum import Enum

from pydantic import BaseModel, HttpUrl


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class ScrapeRequest(BaseModel):
    url: HttpUrl


class ScrapedData(BaseModel):
    title: str | None = None
    authors: list[str] | None = None
    publish_date: datetime | None = None
    text: str | None = None
    keywords: list[str] | None = None
    summary: str | None = None
    url: str


class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    result: ScrapedData | None = None
    error: str | None = None
