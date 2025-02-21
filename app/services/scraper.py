import logging

import newspaper
import nltk

from app.core.celery import celery_app

logger = logging.getLogger(__name__)

nltk.download("punkt_tab")


@celery_app.task(name="app.services.scraper.scrape_url")
def scrape_url(url: str) -> dict:
    logger.info(f"Starting to scrape URL: {url}")
    try:
        article = newspaper.Article(url)
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
        logger.error(f"Failed to scrape URL {url}: {str(e)}")
        raise Exception(f"Failed to scrape URL: {str(e)}")
