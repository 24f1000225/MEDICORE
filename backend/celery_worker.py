from celery import Celery
from backend.config import Config
from celery.schedules import crontab

celery = Celery(
    "hospital_tasks",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True
)

celery.autodiscover_tasks(["backend.tasks"])

# IMPORTANT: explicitly load task modules
celery.conf.imports = (
    "backend.tasks.export_csv",
    "backend.tasks.reminders",
    "backend.tasks.reports",
)

celery.conf.beat_schedule = {
    "daily-patient-reminders": {
        "task": "backend.tasks.reminders.send_daily_reminders",
        "schedule": crontab(hour=8, minute=0),
    },
    "monthly-doctor-reports": {
        "task": "backend.tasks.reports.send_monthly_reports",
        "schedule": crontab(day_of_month=1,hour=9,minute=0),
    },
}