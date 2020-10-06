from celery import Celery

from tasks import fibonacci_task


def start_celery_long_task():
    fibonacci_task.apply_async((1500, 'task-2', '/aged'))


if __name__ == "__main__":
    start_celery_long_task()
