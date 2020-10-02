import numpy
from billiard.process import current_process
from celery import Celery
import time
from flask_socketio import SocketIO
from numpy import argsort

from app import applogger
import os
import subprocess

celery = Celery('demo', broker='redis://localhost:6379')

socketio = SocketIO(message_queue='redis://')


def send_message(event, namespace, room, message):
    print(message)
    socketio.emit(event, {'msg': message}, namespace=namespace, room=room)


def set_cpu_limit(limit: int, task_pid):
    '''
    param limit: should be from 1 to 100 to limit current process
    '''
    os.system(f"cpulimit -l {limit} -p {task_pid}")


def cpu_unlimit(task_pid):
    os.system(f"cpulimit -l 100 -p {task_pid}")


@celery.task
def long_task(n, session, task_event, namespace):
    applogger.info("start long_task")
    applogger.info(f'proc index {os.getpid() }')
    task_pid = os.getpid()
    limit_task_cpu_to = 50
    set_cpu_limit(limit_task_cpu_to, task_pid)
    room = session
    namespace = '/long_task'

    send_message('status', namespace, room, 'Begin')
    send_message(task_event, namespace, room, 'Begin task {}'.format(long_task.request.id))
    send_message(task_event, namespace, room, 'This task will take {} seconds.'.format(n))

    for i in range(n):
        send_message(task_event, namespace, room, str(i))
        time.sleep(1)

    send_message(task_event, namespace, room, 'End Task {}'.format(long_task.request.id))
    send_message('status', namespace, room, 'End')
    cpu_unlimit(task_pid)
    applogger.info("end long_task")


@celery.task
def fibonacci_task(n, session, task_event, namespace):
    room = session
    applogger.info("start fibonacci_task")
    namespace = '/long_task'

    task_pid = os.getpid()
    limit_task_cpu_to = 10
    applogger.info(set_cpu_limit(limit_task_cpu_to, task_pid))

    send_message('status', namespace, room, 'Begin')
    send_message(task_event, namespace, room, 'Begin task {}'.format(fibonacci_task.request.id))
    n1, n2 = 0, 1
    count = 0

    # check if the number of terms is valid
    if n <= 0:
        pass
    elif n == 1:
        send_message(task_event, namespace, room, str(n1))
    else:
        while count < n:
            send_message(task_event, namespace, room, str(n1)[0:20])
            nth = n1 + n2
            # update values
            n1 = n2
            n2 = nth
            count += 1
    send_message(task_event, namespace, room, 'End Task {}'.format(fibonacci_task.request.id))
    send_message('status', namespace, room, 'End')
    applogger.info("end fibonacci_task")
    cpu_unlimit(task_pid)


@celery.task
def matrix_task(session, task_event, namespace):

    applogger.info("start matrix_task")
    room = session
    namespace = '/long_task'

    task_pid = os.getpid()
    applogger.info(f'proc matrix index {os.getpid()}')

    limit_task_cpu_to = 10
    set_cpu_limit(limit_task_cpu_to, task_pid)

    send_message('status', namespace, room, 'Begin')
    send_message(task_event, namespace, room, 'Begin task {}'.format(matrix_task.request.id))

    a = numpy.random.rand(10000, 100)
    b = numpy.random.rand(30000, 100)
    c = numpy.dot(b, a.T)
    send_message(task_event, namespace, room, 'Matrices doted')

    send_message(task_event, namespace, room, 'Matrix sorting....')
    sorted = [argsort(j)[:10] for j in c.T]
    send_message(task_event, namespace, room, 'Matrix sorted')

    send_message(task_event, namespace, room, 'End Task {}'.format(matrix_task.request.id))
    send_message('status', namespace, room, 'End')
    applogger.info("end matrix_task")
