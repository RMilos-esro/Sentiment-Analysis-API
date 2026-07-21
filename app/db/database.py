import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text

from config import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def test_connection():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT * FROM sentiment;"))
        print("¡Conexión exitosa!")
        print(result.fetchone())

if __name__ == "__main__":
    asyncio.run(test_connection())