"""Create all tables on startup."""
import asyncio

# Import all models so Base.metadata knows about them
import src.agent.db_models
import src.checklist.db_models
import src.purchases.db_models
import src.register.db_models  # noqa: F401  # side-effect import: registers models in Base.metadata
from src.common.base import Base
from src.common.database import engine


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created")

if __name__ == "__main__":
    asyncio.run(init())
