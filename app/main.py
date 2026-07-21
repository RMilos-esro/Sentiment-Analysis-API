from typing import List, Optional

from fastapi import FastAPI
from sqlalchemy import Text, text
import uvicorn

from db.schemas import SentimentCreate
from db.models import SentimentModel
from config import DATABASE_URL 
from db.database import AsyncSessionLocal 

app = FastAPI()

@app.get("/select")
async def select(id:Optional[int] = None):
    async with AsyncSessionLocal() as session:
        if id is not None:
            result = await session.execute(text('SELECT * FROM sentiment WHERE id = :id;'), {"id": id})
        else:
            result = await session.execute(text('SELECT * FROM sentiment;'))
        rows = result.mappings().all()
        return rows
    
@app.post("/analyze", response_model=SentimentCreate, status_code=201)
async def analyze_sentiment(text: str):
    print(f"Received text for sentiment analysis: {text}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)