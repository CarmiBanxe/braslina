"""Create all tables on startup."""
import asyncio
from src.common.database import engine
from src.common.base import Base

# Import all models so Base.metadata knows about them
import src.agent.db_models  # noqa
import src.checklist.db_models  # noqa
import src.register.db_models  # noqa
import src.purchases.db_models  # noqa

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created")

if __name__ == "__main__":
    asyncio.run(init())
