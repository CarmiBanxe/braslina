"""FastAPI router for CRM workflows and reminders."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database import get_db
from src.common.exceptions import InvalidStateTransition, NotFoundError
from src.crm.schemas import (
    ReminderCreate,
    ReminderResponse,
    WorkflowAdvance,
    WorkflowCreate,
    WorkflowResponse,
)
from src.crm.service import CRMService

router = APIRouter()


# --- Workflow endpoints ---

@router.post("/workflow", response_model=WorkflowResponse, status_code=201)
async def create_workflow(data: WorkflowCreate, db: AsyncSession = Depends(get_db)):
    svc = CRMService(db)
    return await svc.create_workflow(**data.model_dump())


@router.get("/workflow/{merchant_id}", response_model=WorkflowResponse)
async def get_workflow(merchant_id: str, db: AsyncSession = Depends(get_db)):
    svc = CRMService(db)
    try:
        return await svc.get_workflow(merchant_id)
    except NotFoundError as exc:
        raise HTTPException(404, detail=exc.message)


@router.patch("/workflow/{merchant_id}/advance", response_model=WorkflowResponse)
async def advance_workflow(
    merchant_id: str, data: WorkflowAdvance, db: AsyncSession = Depends(get_db)
):
    svc = CRMService(db)
    try:
        return await svc.advance_workflow(merchant_id, data.new_stage, data.assignee_id)
    except NotFoundError as exc:
        raise HTTPException(404, detail=exc.message)
    except InvalidStateTransition as exc:
        raise HTTPException(422, detail=exc.message)


# --- Reminder endpoints ---

@router.post("/{merchant_id}/remind", response_model=ReminderResponse, status_code=201)
async def schedule_reminder(
    merchant_id: str, data: ReminderCreate, db: AsyncSession = Depends(get_db)
):
    svc = CRMService(db)
    return await svc.schedule_reminder(
        merchant_id=merchant_id,
        message=data.message,
        scheduled_at=data.scheduled_at,
        channel=data.channel,
    )


@router.get("/{merchant_id}/reminders", response_model=list[ReminderResponse])
async def list_reminders(merchant_id: str, db: AsyncSession = Depends(get_db)):
    svc = CRMService(db)
    return await svc.list_reminders(merchant_id)
