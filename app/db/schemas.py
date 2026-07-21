from pydantic import BaseModel, Field

class SentimentCreate(BaseModel):
    text: str = Field(..., max_length=255)

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    score: float

    class Config:
        from_attributes = True 