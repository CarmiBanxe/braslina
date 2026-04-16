"""FastAPI router for website monitor agent."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database import get_db
from src.agent.db_models import SnapshotDB
from src.agent.schemas import MonitorRequest, MonitorResult, SnapshotResponse
from src.agent.monitor import monitor_merchant

router = APIRouter()

STORAGE_DIR = Path("/app/storage/screenshots")


@router.post("/monitor", response_model=MonitorResult)
async def run_monitor(req: MonitorRequest, db: AsyncSession = Depends(get_db)):
    result = await monitor_merchant(
        merchant_id=req.merchant_id,
        url=req.url,
        storage_dir=STORAGE_DIR,
        alert_threshold_pct=req.alert_threshold_pct,
    )
    snapshot = SnapshotDB(
        merchant_id=req.merchant_id,
        screenshot_url=result.get("diff_path", ""),
        diff_url=result.get("diff_path"),
        diff_pct=result.get("diff_pct"),
        alert_triggered=result.get("alert", False),
    )
    db.add(snapshot)
    await db.commit()
    return MonitorResult(
        merchant_id=req.merchant_id,
        action=result.get("action"),
        diff_pct=result.get("diff_pct"),
        alert=result.get("alert", False),
        screenshot_url=result.get("diff_path"),
        diff_url=result.get("diff_path"),
    )


@router.get("/snapshots/{merchant_id}", response_model=list[SnapshotResponse])
async def list_snapshots(merchant_id: str, db: AsyncSession = Depends(get_db)):
    q = select(SnapshotDB).where(SnapshotDB.merchant_id == merchant_id).order_by(SnapshotDB.created_at.desc())
    result = await db.execute(q)
    return result.scalars().all()
