import asyncio
from book_management_system.app.database import engine
from book_management_system.app.models import Base

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_tables())