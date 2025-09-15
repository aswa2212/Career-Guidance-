import logging
from fastapi import BackgroundTasks

logger = logging.getLogger(__name__)

async def send_notification(user_id: int, title: str, message: str):
    # In a real application, this would send an email or push notification
    # For now, we'll just log it
    logger.info(f"Notification for user {user_id}: {title} - {message}")