"""Monitor service — orchestrates screenshot, diff, storage, and alerting."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.agent.db_models import SnapshotDB
from src.agent.monitor import ScreenshotResult, capture_and_diff
from src.agent.repository import SnapshotRepository
from src.common.config import settings


class MonitorService:
    def __init__(self, db: AsyncSession):
        self.repo = SnapshotRepository(db)

    async def run_monitor(self, merchant_id: str, url: str) -> tuple[SnapshotDB, bool]:
        """Capture screenshot, diff against previous, store snapshot, return (snapshot, alert_triggered)."""
        previous = await self.repo.get_latest(merchant_id)
        previous_path = previous.screenshot_url if previous else None

        result: ScreenshotResult = await capture_and_diff(
            merchant_id=merchant_id,
            url=url,
            previous_screenshot_path=previous_path,
        )

        alert_triggered = result.diff_pct > settings.ALERT_THRESHOLD_PCT if result.diff_pct is not None else False

        snapshot = SnapshotDB(
            merchant_id=merchant_id,
            screenshot_url=result.screenshot_path,
            diff_url=result.diff_path,
            diff_pct=result.diff_pct or 0.0,
            alert_triggered=alert_triggered,
        )
        snapshot = await self.repo.create(snapshot)
        return snapshot, alert_triggered

    async def list_snapshots(self, merchant_id: str) -> list[SnapshotDB]:
        return await self.repo.list_by_merchant(merchant_id)

    async def get_latest(self, merchant_id: str) -> SnapshotDB | None:
        return await self.repo.get_latest(merchant_id)
