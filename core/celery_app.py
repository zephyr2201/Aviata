import os

from celery import Celery

from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("aviata")

app.config_from_object("core.settings", namespace="CELERY")
app.conf.task_default_queue = "default"

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {

    'get-currency': {
        'task': 'airflow.tasks.request_for_currency',
        'schedule': crontab(hour='12', minute='0')
    },

}

app.conf.timezone = "Asia/Almaty"
