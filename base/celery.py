import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")


app = Celery("base", broker="redis://localhost:6379")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf.settings", namespace="CELERY")
app.conf.broker_url = settings.CELERY_BROKER_URL

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.update(timezone="Europe/Kyiv")


app.conf.beat_schedule = {
    "send_news_every_5_minutes": {
        "task": "users.tasks.send_news_email",
        "schedule": crontab(minute="*/2"),
    }
}

app.conf.timezone = "UTC"
