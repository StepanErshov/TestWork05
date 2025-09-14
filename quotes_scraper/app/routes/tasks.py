from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from ..celery_app import celery_app
from ..models import TaskResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/parse-quotes-task", response_model=TaskResponse)
async def parse_quotes_task():
    try:
        task = celery_app.send_task("scrape_and_save_quotes")
        logger.info(f"Started Celery task with ID: {task.id}")
        
        return TaskResponse(task_id=task.id)
        
    except Exception as e:
        logger.error(f"Error starting scraping task: {e}")
        raise HTTPException(status_code=500, detail=f"Error starting task: {str(e)}")

@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        return {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting task status: {str(e)}")
