from typing import Optional

from pydantic import BaseModel, Field

class SentimentCreate(BaseModel):
    text: str = Field(...,min_length=10, max_length=255)
    sentiment: Optional[str] = Field(..., min_length=1, max_length=50)
    score: Optional[float] = Field(..., ge=0.0, le=1.0)
    language: Optional[str] = Field(..., min_length=2, max_length=2)  

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    score: float
    language: str

    class Config:
        from_attributes = True 