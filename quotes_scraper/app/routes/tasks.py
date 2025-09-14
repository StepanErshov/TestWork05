from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from ..celery_worker import celery_app
from ..models import TaskResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/parse-quotes-task", response_model=TaskResponse)
async def parse_quotes_task():
    """
    Start a Celery task to scrape quotes and save to MongoDB
    """
    try:
        # Start the Celery task
        task = celery_app.send_task("scrape_and_save_quotes")
        logger.info(f"Started Celery task with ID: {task.id}")
        
        return TaskResponse(task_id=task.id)
        
    except Exception as e:
        logger.error(f"Error starting scraping task: {e}")
        raise HTTPException(status_code=500, detail=f"Error starting task: {str(e)}")