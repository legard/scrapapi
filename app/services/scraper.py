import logging

import newspaper
import nltk
from celery import current_task
from newspaper.configuration import Configuration
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.celery import celery_app
from app.core.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

nltk.download("punkt_tab")


@retry(
    wait=wait_exponential(multiplier=5, min=5, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(Exception),
    before_sleep=lambda retry_state: logger.warning(
        f"Task ID: {current_task.request.id if current_task else 'N/A'}, "
        f"Attempt: {retry_state.attempt_number}/{retry_state.retry_object.stop.max_attempt_number if isinstance(retry_state.retry_object.stop, stop_after_attempt) else 'N/A'}, "
        f"Next retry in: {retry_state.next_action.sleep if retry_state.next_action else 'N/A'} seconds, "
        f"Exception: {retry_state.outcome.exception() if retry_state.outcome else 'None'}"
    ),
    after=lambda retry_state: logger.warning(
        f"Task ID: {current_task.request.id if current_task else 'N/A'}, "
        f"Final attempt: {retry_state.attempt_number}, "
        f"Succeeded: {retry_state.outcome and retry_state.outcome.failed is False}, "
        f"Exception: {retry_state.outcome.exception() if retry_state.outcome and retry_state.outcome.failed else 'None'}"
    )
    if isinstance(retry_state.retry_object.stop, stop_after_attempt)
    and retry_state.attempt_number >= retry_state.retry_object.stop.max_attempt_number
    else None,
)
def scrape_url_with_retry(url: str) -> dict:
    logger.info(f"Starting to scrape URL: {url}")
    try:
        config = Configuration()

        if settings.HTTP_PROXY:
            logger.info(f"Using HTTP proxy: {settings.HTTP_PROXY}")
            config.browser_user_agent = "Mozilla/5.0"
            config.proxies = {
                "http": settings.HTTP_PROXY,
                "https": settings.HTTPS_PROXY or settings.HTTP_PROXY,
            }

        article = newspaper.Article(url, config=config)
        article.download()
        article.parse()
        article.nlp()

        result = {
            "title": article.title,
            "authors": article.authors,
            "publish_date": article.publish_date.isoformat()
            if article.publish_date
            else None,
            "text": article.text,
            "keywords": article.keywords,
            "summary": article.summary,
            "url": url,
        }
        logger.info(f"Successfully scraped URL: {url}")
        return result
    except Exception as e:
        logger.error(
            f"Task ID: {current_task.request.id if current_task else 'N/A'}, Failed to scrape URL {url}: {str(e)}"
        )
        raise Exception(f"Failed to scrape URL: {str(e)}")


@celery_app.task(name="app.services.scraper.scrape_url")
def scrape_url(url: str) -> dict:
    task_id = current_task.request.id if current_task else "N/A"
    logger.info(f"Starting task {task_id} for URL: {url}")
    try:
        result = scrape_url_with_retry(url)
        logger.info(f"Task {task_id} completed successfully")
        return result
    except Exception as e:
        logger.error(f"Task {task_id} failed with exception: {str(e)}")
        raise
