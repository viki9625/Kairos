# Celery worker stub — configure broker=redis://... in production
from celery import Celery
from core.config import settings


celery = Celery(__name__, broker=settings.redis_url, backend=settings.redis_url)


@celery.task
def notify_moderators(message_id: str):
    print(f"[task] notify moderators about message {message_id}")
# integrate email/webhook/slack here