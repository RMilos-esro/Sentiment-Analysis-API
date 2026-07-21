from typing import List, Optional

from fastapi import FastAPI, HTTPException
from sqlalchemy import Text, text
import uvicorn
from datetime import datetime, timezone
from app.db.schemas import SentimentCreate
from app.db.models import SentimentModel
from config import DATABASE_URL 
from app.db.database import AsyncSessionLocal 
from app.nlp.sentiment import analyze_sentiment_by_lang
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sentiment Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

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
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)