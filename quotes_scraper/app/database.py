from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "quotes_db")

client = AsyncIOMotorClient(MONGO_URL)
database = client[MONGO_DB_NAME]
quotes_collection = database.quotes
