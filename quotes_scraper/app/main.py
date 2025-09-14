from fastapi import FastAPI
from .routes import quotes, tasks
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Quotes Scraper API",
    description="API for scraping and retrieving quotes from quotes.toscrape.com",
    version="1.0.0"
)

app.include_router(tasks.router, prefix="", tags=["tasks"])
app.include_router(quotes.router, prefix="", tags=["quotes"])

@app.get("/")
async def root():
    return {"message": "Quotes Scraper API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}