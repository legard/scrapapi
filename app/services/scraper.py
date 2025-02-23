import logging

import newspaper
import nltk
from newspaper.configuration import Configuration

from app.core.celery import celery_app
from app.core.config import settings

logger = logging.getLogger(__name__)

nltk.download("punkt_tab")


@celery_app.task(name="app.services.scraper.scrape_url")
def scrape_url(url: str) -> dict:
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
            "link": url,
        }
        logger.info(f"Successfully scraped URL: {url}")
        return result
    except Exception as e:
        logger.error(f"Failed to scrape URL {url}: {str(e)}")
        raise Exception(f"Failed to scrape URL: {str(e)}")
