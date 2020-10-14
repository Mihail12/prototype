from datetime import timedelta

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'tasks.schedule_task',
        'schedule': timedelta(seconds=10),
        'args': ('task-5', '/schedule_task')
    },
}
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']