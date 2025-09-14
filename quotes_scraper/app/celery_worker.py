from celery_app import celery_app
from datetime import datetime
from .scraper import scrape_quotes
from .database import quotes_collection
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="scrape_and_save_quotes")
def scrape_and_save_quotes():
    try:
        logger.info("Starting quote scraping task...")
        
        quotes = scrape_quotes()
        
        if not quotes:
            logger.warning("No quotes were scraped")
            return {"status": "completed", "quotes_count": 0}
        
        logger.info(f"Scraped {len(quotes)} quotes, starting to save to MongoDB...")
        
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
        else:
            logger.warning("No documents to insert")
            return {"status": "completed", "quotes_count": 0}
            
    except Exception as e:
        logger.error(f"Error in scraping task: {str(e)}")
        logger.exception("Full traceback:")
        return {"status": "failed", "error": str(e)}
