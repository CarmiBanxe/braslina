"""FastAPI router for merchant checklists."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.checklist.schemas import (
    CheckItemResponse,
    CheckItemUpdate,
    ChecklistCreate,
    ChecklistResponse,
    EvaluationResponse,
)
from src.checklist.service import ChecklistService
from src.common.database import get_db
from src.common.exceptions import InvalidStateTransition, NotFoundError

router = APIRouter()


def _svc(db: AsyncSession = Depends(get_db)) -> ChecklistService:
    return ChecklistService(db)


@router.post("/", response_model=ChecklistResponse, status_code=201)
async def create_checklist(data: ChecklistCreate, svc: ChecklistService = Depends(_svc)):
    return await svc.create_from_template(data.merchant_id, data.template_id)


@router.get("/{checklist_id}", response_model=ChecklistResponse)
async def get_checklist(checklist_id: str, svc: ChecklistService = Depends(_svc)):
    try:
        return await svc.get_checklist(checklist_id)
    except NotFoundError as e:
        raise HTTPException(404, e.message) from None


@router.get("/merchant/{merchant_id}", response_model=list[ChecklistResponse])
async def list_checklists_by_merchant(merchant_id: str, svc: ChecklistService = Depends(_svc)):
    return await svc.list_by_merchant(merchant_id)


@router.patch("/items/{item_id}", response_model=CheckItemResponse)
async def update_check_item(item_id: str, data: CheckItemUpdate, svc: ChecklistService = Depends(_svc)):
    try:
        return await svc.update_item_status(
            item_id, data.status.value, data.evidence_url, data.notes
        )
    except NotFoundError as e:
        raise HTTPException(404, e.message) from None
    except InvalidStateTransition as e:
        raise HTTPException(422, e.message) from None


@router.post("/evaluate/{checklist_id}", response_model=EvaluationResponse)
async def evaluate_checklist(checklist_id: str, svc: ChecklistService = Depends(_svc)):
    try:
        result = await svc.evaluate_checklist(checklist_id)
        return EvaluationResponse(
            total=result.total,
            passed=result.passed,
            failed=result.failed,
            needs_review=result.needs_review,
            pending=result.pending,
            not_applicable=result.not_applicable,
            is_complete=result.is_complete,
            is_blocked=result.is_blocked,
            completion_pct=result.completion_pct,
        )
    except NotFoundError as e:
        raise HTTPException(404, e.message) from None
