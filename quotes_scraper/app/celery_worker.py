from celery import Celery
import os
from datetime import datetime
from .scraper import scrape_quotes
from .database import quotes_collection
import logging

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "quotes_scraper",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery_app.task
def scrape_and_save_quotes():
    try:
        logger.info("Starting quote scraping task...")
        
        quotes = scrape_quotes()
        
        if not quotes:
            logger.warning("No quotes were scraped")
            return {"status": "completed", "quotes_count": 0}
        
        documents = []
        for quote in quotes:
            document = {
                **quote,
                "created_at": datetime.utcnow()
            }
            documents.append(document)
        
        if documents:
            result = quotes_collection.insert_many(documents)
            logger.info(f"Successfully inserted {len(result.inserted_ids)} quotes into MongoDB")
        
        return {"status": "completed", "quotes_count": len(quotes)}
        
    except Exception as e:
        logger.error(f"Error in scraping task: {e}")
        return {"status": "failed", "error": str(e)}