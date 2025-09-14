from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Quote(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    author: str
    quote: str
    tags: List[str]
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class QuoteCreate(BaseModel):
    author: str
    quote: str
    tags: List[str]

class TaskResponse(BaseModel):
    task_id: str