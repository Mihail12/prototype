from datetime import timedelta

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'tasks.schedule_task',
        'schedule': timedelta(seconds=30),
        'args': ('task-5', '/schedule_task')
    }
}