"""Seed data for local development."""

import asyncio

from src.common.database import async_session
from src.register.db_models import MerchantDB

SEED_MERCHANTS = [
    {"name": "Test Merchant Alpha", "website": "https://alpha-shop.example.com", "mcc": "5411"},
    {"name": "Test Merchant Beta", "website": "https://beta-store.example.com", "mcc": "5812"},
    {"name": "Test Merchant Gamma", "website": "https://gamma-pay.example.com", "mcc": "7011"},
]


async def seed():
    async with async_session() as db:
        for data in SEED_MERCHANTS:
            merchant = MerchantDB(**data)
            db.add(merchant)
        await db.commit()
        print(f"Seeded {len(SEED_MERCHANTS)} merchants")


if __name__ == "__main__":
    asyncio.run(seed())
