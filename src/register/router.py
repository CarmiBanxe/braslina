"""FastAPI router for merchant register."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database import get_db
from src.register.db_models import MerchantDB
from src.register.schemas import MerchantCreate, MerchantUpdate, MerchantResponse

router = APIRouter()


@router.get("/", response_model=list[MerchantResponse])
async def list_merchants(status: str | None = None, db: AsyncSession = Depends(get_db)):
    q = select(MerchantDB)
    if status:
        q = q.where(MerchantDB.status == status)
    q = q.order_by(MerchantDB.created_at.desc())
    result = await db.execute(q)
    return result.scalars().all()


@router.post("/", response_model=MerchantResponse, status_code=201)
async def create_merchant(data: MerchantCreate, db: AsyncSession = Depends(get_db)):
    merchant = MerchantDB(**data.model_dump())
    db.add(merchant)
    await db.commit()
    await db.refresh(merchant)
    return merchant


@router.get("/{merchant_id}", response_model=MerchantResponse)
async def get_merchant(merchant_id: str, db: AsyncSession = Depends(get_db)):
    merchant = await db.get(MerchantDB, merchant_id)
    if not merchant:
        raise HTTPException(404, "Merchant not found")
    return merchant


@router.patch("/{merchant_id}", response_model=MerchantResponse)
async def update_merchant(merchant_id: str, data: MerchantUpdate, db: AsyncSession = Depends(get_db)):
    merchant = await db.get(MerchantDB, merchant_id)
    if not merchant:
        raise HTTPException(404, "Merchant not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(merchant, k, v)
    await db.commit()
    await db.refresh(merchant)
    return merchant


@router.delete("/{merchant_id}", status_code=204)
async def delete_merchant(merchant_id: str, db: AsyncSession = Depends(get_db)):
    merchant = await db.get(MerchantDB, merchant_id)
    if not merchant:
        raise HTTPException(404, "Merchant not found")
    await db.delete(merchant)
    await db.commit()
