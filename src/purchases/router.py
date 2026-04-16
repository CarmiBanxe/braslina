"""FastAPI router for test purchases."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database import get_db
from src.purchases.db_models import TestPurchaseDB
from src.purchases.schemas import PurchaseCreate, PurchaseResponse

router = APIRouter()


@router.get("/merchant/{merchant_id}", response_model=list[PurchaseResponse])
async def list_purchases(merchant_id: str, db: AsyncSession = Depends(get_db)):
    q = select(TestPurchaseDB).where(TestPurchaseDB.merchant_id == merchant_id).order_by(TestPurchaseDB.performed_at.desc())
    result = await db.execute(q)
    return result.scalars().all()


@router.post("/", response_model=PurchaseResponse, status_code=201)
async def create_purchase(data: PurchaseCreate, db: AsyncSession = Depends(get_db)):
    purchase = TestPurchaseDB(**data.model_dump())
    db.add(purchase)
    await db.commit()
    await db.refresh(purchase)
    return purchase


@router.get("/{purchase_id}", response_model=PurchaseResponse)
async def get_purchase(purchase_id: str, db: AsyncSession = Depends(get_db)):
    purchase = await db.get(TestPurchaseDB, purchase_id)
    if not purchase:
        raise HTTPException(404, "Purchase not found")
    return purchase
