"""FastAPI router for merchant checklists."""

import copy
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.common.database import get_db
from src.checklist.db_models import ChecklistDB, CheckItemDB
from src.checklist.engine import SALES_CHECKLIST
from src.checklist.schemas import ChecklistCreate, ChecklistResponse, CheckItemUpdate, CheckItemResponse

router = APIRouter()


@router.post("/", response_model=ChecklistResponse, status_code=201)
async def create_checklist(data: ChecklistCreate, db: AsyncSession = Depends(get_db)):
    template = SALES_CHECKLIST  # TODO: lookup by template_id
    checklist = ChecklistDB(merchant_id=data.merchant_id, template_id=data.template_id)
    for item in template.items:
        checklist.items.append(CheckItemDB(
            name=item.name, description=item.description,
            auto_verifiable=item.auto_verifiable,
        ))
    db.add(checklist)
    await db.commit()
    await db.refresh(checklist, ["items"])
    return checklist


@router.get("/{checklist_id}", response_model=ChecklistResponse)
async def get_checklist(checklist_id: str, db: AsyncSession = Depends(get_db)):
    q = select(ChecklistDB).where(ChecklistDB.id == checklist_id).options(selectinload(ChecklistDB.items))
    result = await db.execute(q)
    checklist = result.scalar_one_or_none()
    if not checklist:
        raise HTTPException(404, "Checklist not found")
    return checklist


@router.get("/merchant/{merchant_id}", response_model=list[ChecklistResponse])
async def list_checklists_by_merchant(merchant_id: str, db: AsyncSession = Depends(get_db)):
    q = select(ChecklistDB).where(ChecklistDB.merchant_id == merchant_id).options(selectinload(ChecklistDB.items))
    result = await db.execute(q)
    return result.scalars().all()


@router.patch("/items/{item_id}", response_model=CheckItemResponse)
async def update_check_item(item_id: str, data: CheckItemUpdate, db: AsyncSession = Depends(get_db)):
    item = await db.get(CheckItemDB, item_id)
    if not item:
        raise HTTPException(404, "Check item not found")
    item.status = data.status
    item.verified_at = datetime.now(timezone.utc)
    if data.evidence_url is not None:
        item.evidence_url = data.evidence_url
    if data.notes is not None:
        item.notes = data.notes
    await db.commit()
    await db.refresh(item)
    return item
