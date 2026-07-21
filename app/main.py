from typing import List, Optional

from fastapi import FastAPI, HTTPException
from sqlalchemy import Text, text
import uvicorn
from datetime import datetime, timezone
from db.schemas import SentimentCreate
from db.models import SentimentModel
from config import DATABASE_URL 
from db.database import AsyncSessionLocal 
from nlp.sentiment import analyze_sentiment_by_lang

app = FastAPI(title="Sentiment Analysis API")


@app.get("/history")
async def get_history(id:Optional[int] = None):
    async with AsyncSessionLocal() as session:
        if id is not None:
            result = await session.execute(text('SELECT * FROM sentiment WHERE id = :id;'), {"id": id})
        else:
            result = await session.execute(text('SELECT * FROM sentiment;'))
        rows = result.mappings().all()
        return rows
    
@app.post("/analyze", response_model=SentimentCreate, status_code=201)
async def analyze_sentiment(text: str):
    result = analyze_sentiment_by_lang(text)
    if not result['supported']:
        raise HTTPException(status_code=400, detail=result['error'])
    
    
    resultDB = SentimentModel(
        text=text,
        sentiment=result['label'],
        score=result['score'],
        date=datetime.now(timezone.utc),
        language=result['language']
    )

    async with AsyncSessionLocal() as session:
        session.add(resultDB)
        await session.commit()
        await session.refresh(resultDB)

    return {
        "text": text,
        "sentiment": result['label'],
        "score": result['score'],
        "language": result['language']
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)