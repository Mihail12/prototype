from tasks import long_task


def start_celery_long_task():
    long_task.apply_async((10, 'task-1', '/managers'))


if __name__ == "__main__":
    start_celery_long_task()
