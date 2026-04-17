"""FastAPI router for test purchases."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.database import get_db
from src.common.exceptions import NotFoundError, ValidationError
from src.purchases.schemas import PurchaseCreate, PurchaseResponse, PurchaseSummary
from src.purchases.service import PurchaseService

router = APIRouter()


@router.get("/merchant/{merchant_id}", response_model=list[PurchaseResponse])
async def list_purchases(merchant_id: str, db: AsyncSession = Depends(get_db)):
    svc = PurchaseService(db)
    return await svc.list_purchases(merchant_id)


@router.post("/", response_model=PurchaseResponse, status_code=201)
async def create_purchase(data: PurchaseCreate, db: AsyncSession = Depends(get_db)):
    svc = PurchaseService(db)
    try:
        return await svc.create_purchase(**data.model_dump())
    except ValidationError as exc:
        raise HTTPException(422, detail=exc.message) from exc


@router.get("/{purchase_id}", response_model=PurchaseResponse)
async def get_purchase(purchase_id: str, db: AsyncSession = Depends(get_db)):
    svc = PurchaseService(db)
    try:
        return await svc.get_purchase(purchase_id)
    except NotFoundError as exc:
        raise HTTPException(404, detail=exc.message) from exc


@router.get("/summary/{merchant_id}", response_model=PurchaseSummary)
async def purchase_summary(merchant_id: str, db: AsyncSession = Depends(get_db)):
    svc = PurchaseService(db)
    return await svc.get_summary(merchant_id)
