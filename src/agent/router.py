"""FastAPI router for website monitor agent."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.agent.schemas import MonitorRequest, MonitorResult, SnapshotResponse
from src.agent.service import MonitorService
from src.common.database import get_db

router = APIRouter()


def _svc(db: AsyncSession = Depends(get_db)) -> MonitorService:
    return MonitorService(db)


@router.post("/monitor", response_model=MonitorResult)
async def run_monitor(req: MonitorRequest, svc: MonitorService = Depends(_svc)):
    snapshot, alert_triggered = await svc.run_monitor(req.merchant_id, req.url)
    return MonitorResult(
        merchant_id=req.merchant_id,
        action="captured",
        diff_pct=snapshot.diff_pct,
        alert=alert_triggered,
        screenshot_url=snapshot.screenshot_url,
        diff_url=snapshot.diff_url,
    )


@router.get("/snapshots/{merchant_id}", response_model=list[SnapshotResponse])
async def list_snapshots(merchant_id: str, svc: MonitorService = Depends(_svc)):
    return await svc.list_snapshots(merchant_id)
