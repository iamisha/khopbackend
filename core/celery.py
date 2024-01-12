import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send-recommendation-to-parents': {
        'task': 'recommendation.tasks.send_recommendation_to_parents',
        # 'schedule': crontab(day_of_week='sunday', hour=6, minute=0),  
        'schedule': crontab(minute="*/3"),  
    },
    'send-vaccine-reminder': {
        "task": "recommendation.tasks.send_vaccination_notifications",
        # "schedule": crontab(hour=23, minute=59),
        'schedule': crontab(minute="*/3"),  

    },
}

app.autodiscover_tasks()
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')