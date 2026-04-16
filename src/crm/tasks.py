"""Celery tasks for CRM reminders."""
import logging
from datetime import datetime

from src.celery_app import app

logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_reminder(self, reminder_id: str, merchant_id: str, message: str, channel: str):
    """Send a reminder via the specified channel.

    In MVP this just logs the reminder. Future: email/Slack integration.
    """
    try:
        logger.info(
            "Sending reminder %s for merchant %s via %s: %s",
            reminder_id,
            merchant_id,
            channel,
            message,
        )
        # TODO: implement email/slack dispatch based on channel
        return {
            "reminder_id": reminder_id,
            "merchant_id": merchant_id,
            "channel": channel,
            "status": "sent",
            "sent_at": datetime.utcnow().isoformat(),
        }
    except Exception as exc:
        logger.error("Failed to send reminder %s: %s", reminder_id, exc)
        raise self.retry(exc=exc)


@app.task
def process_pending_reminders():
    """Scan for unsent reminders past their scheduled_at and dispatch them.

    Called by Celery Beat on schedule.
    """
    # TODO: query DB for pending reminders, call send_reminder for each
    logger.info("Processing pending reminders")
    return {"status": "ok", "message": "pending reminders processed"}
