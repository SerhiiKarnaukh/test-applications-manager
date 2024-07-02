from celery import Celery
import os
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

app = Celery('portfolio')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'create_social_posts_trends': {
        'task': 'social_posts.tasks.create_social_posts_trends',
        'schedule': crontab(hour=4, minute=0),
        'options': {'timezone': 'Europe/Kiev'},
    },
    'create_social_friend_suggestions': {
        'task': 'social_profiles.tasks.create_social_friend_suggestions',
        'schedule': crontab(hour=5, minute=0),
        'options': {'timezone': 'Europe/Kiev'},
    },
}
