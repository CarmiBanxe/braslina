"""FastAPI router for merchant register."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database import get_db
from src.common.exceptions import InvalidStateTransition, NotFoundError
from src.register.schemas import (
    MerchantCreate,
    MerchantDetailResponse,
    MerchantResponse,
    MerchantUpdate,
    StatusChangeRequest,
)
from src.register.service import RegisterService

router = APIRouter()


def _svc(db: AsyncSession = Depends(get_db)) -> RegisterService:
    return RegisterService(db)


@router.get("/", response_model=list[MerchantResponse])
async def list_merchants(status: str | None = None, svc: RegisterService = Depends(_svc)):
    return await svc.list_merchants(status)


@router.post("/", response_model=MerchantResponse, status_code=201)
async def create_merchant(data: MerchantCreate, svc: RegisterService = Depends(_svc)):
    return await svc.create_merchant(data.name, data.website, data.mcc)


@router.get("/{merchant_id}", response_model=MerchantDetailResponse)
async def get_merchant(merchant_id: str, svc: RegisterService = Depends(_svc)):
    try:
        return await svc.get_merchant(merchant_id)
    except NotFoundError as e:
        raise HTTPException(404, e.message) from None


@router.patch("/{merchant_id}", response_model=MerchantResponse)
async def update_merchant(merchant_id: str, data: MerchantUpdate, svc: RegisterService = Depends(_svc)):
    try:
        merchant = await svc.get_merchant(merchant_id)
    except NotFoundError as e:
        raise HTTPException(404, e.message) from None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(merchant, field, value)
    from src.register.repository import MerchantRepository
    repo = MerchantRepository(svc.db)
    return await repo.update(merchant)


@router.patch("/{merchant_id}/status", response_model=MerchantResponse)
async def change_merchant_status(
    merchant_id: str, data: StatusChangeRequest, svc: RegisterService = Depends(_svc)
):
    try:
        return await svc.change_status(merchant_id, data.status.value, data.changed_by, data.reason)
    except NotFoundError as e:
        raise HTTPException(404, e.message) from None
    except InvalidStateTransition as e:
        raise HTTPException(422, e.message) from None


@router.delete("/{merchant_id}", status_code=204)
async def delete_merchant(merchant_id: str, svc: RegisterService = Depends(_svc)):
    try:
        await svc.delete_merchant(merchant_id)
    except NotFoundError as e:
        raise HTTPException(404, e.message) from None
