import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')

app = Celery('home')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "run_movie_rating_avg_every_30" : {
        'task': 'task_calculate_movie_ratings',
        'schedule': 30 * 60, #30 secs
        'kwargs': {'count': 100}
    }
}

