from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..database import quotes_collection
from ..models import Quote
from bson import ObjectId
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def quote_helper(quote) -> dict:
    return {
        "id": str(quote["_id"]),
        "author": quote["author"],
        "quote": quote["quote"],
        "tags": quote["tags"],
        "created_at": quote["created_at"]
    }

@router.get("/quotes", response_model=List[Quote])
async def get_quotes(
    author: Optional[str] = Query(None, description="Filter by author"),
    tag: Optional[str] = Query(None, description="Filter by tag")
):
    try:
        query = {}
        if author:
            query["author"] = {"$regex": author, "$options": "i"}
        if tag:
            query["tags"] = tag
        
        logger.info(f"Querying quotes with filters: {query}")
        
        cursor = quotes_collection.find(query).sort("created_at", -1)
        quotes = []
        async for document in cursor:
            quotes.append(quote_helper(document))
        
        if not quotes:
            logger.info("No quotes found matching the criteria")
            raise HTTPException(
                status_code=404,
                detail="No quotes found matching the specified criteria"
            )
        
        logger.info(f"Found {len(quotes)} quotes")
        return quotes
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving quotes: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving quotes: {str(e)}")
