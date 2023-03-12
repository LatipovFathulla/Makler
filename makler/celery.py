from celery import Celery
import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'makler.settings')
app = Celery('makler')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
