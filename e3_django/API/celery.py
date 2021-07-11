import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e3_django.settings")

app = Celery("e3_django")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
