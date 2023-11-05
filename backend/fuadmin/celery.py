import os

from celery import Celery, platforms
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "fuadmin.settings")

# app = Celery(f"application")
celery_app = Celery(f"system")

celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# app.autodiscover_tasks()
platforms.C_FORCE_ROOT = True
