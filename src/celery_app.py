"""Celery application for Braslina background tasks."""

import os

from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery("braslina", broker=redis_url, backend=redis_url)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

app.conf.beat_schedule = {
    "monitor-merchants-daily": {
        "task": "src.celery_app.monitor_all_merchants",
        "schedule": 86400.0,  # every 24h
    },
}


@app.task
def monitor_all_merchants():
    """Placeholder: iterate merchant registry and run monitor_merchant for each."""
    # TODO: query DB for active merchants, call monitor_merchant per each
    return {"status": "ok", "message": "merchant monitoring cycle complete"}


@app.task
def run_checklist_auto_verify(merchant_id: str, checklist_id: str):
    """Placeholder: run auto-verifiable checks for a merchant checklist."""
    return {"merchant_id": merchant_id, "checklist_id": checklist_id, "status": "verified"}
