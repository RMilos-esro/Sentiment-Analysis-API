from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Float, String, Integer

class Base(DeclarativeBase):
    pass

class SentimentModel(Base):
    __tablename__ = "sentiment"  

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(255))
    sentiment: Mapped[str] = mapped_column(String(50))
    score: Mapped[float] = mapped_column(Float)
    date: Mapped[str] = mapped_column(String(50))  