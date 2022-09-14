import os
from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orjah.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('orjah')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()