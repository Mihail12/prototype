import numpy
import time
from flask_socketio import SocketIO
from numpy import argsort
from f_app import celery_app, applogger

import os


socketio = SocketIO(message_queue='redis://')


def send_message(event, namespace, room, message):
    print(message)
    socketio.emit(event, {'msg': message}, namespace=namespace, room=room)


def broadcast_message(event, namespace, message):
    print(message)
    socketio.emit(event, {'msg': message}, namespace=namespace, broadcast=True)


def set_cpu_limit(limit: int, task_pid):
    '''
    param limit: should be from 1 to 100 to limit current process
    '''
    os.system(f"cpulimit -l {limit} -p {task_pid}")


def cpu_unlimit(task_pid):
    os.system(f"cpulimit -l 100 -p {task_pid}")


@celery_app.task
def long_task(n, task_event, namespace):
    applogger.info("start long_task")
    applogger.info(f'proc index {os.getpid() }')
    # task_pid = os.getpid()
    # limit_task_cpu_to = 50
    # set_cpu_limit(limit_task_cpu_to, task_pid)

    broadcast_message('status', namespace, 'Begin')
    broadcast_message(task_event, namespace, 'Begin task {}'.format(long_task.request.id))
    broadcast_message(task_event, namespace, 'This task will take {} seconds.'.format(n))

    for i in range(n):
        broadcast_message(task_event, namespace, str(i))
        time.sleep(1)

    broadcast_message(task_event, namespace, 'End Task {}'.format(long_task.request.id))
    broadcast_message('status', namespace, 'End')
    # cpu_unlimit(task_pid)
    applogger.info("end long_task")
    return 'Done'


@celery_app.task
def fibonacci_task(n, task_event, namespace):
    applogger.info("start fibonacci_task")

    # task_pid = os.getpid()
    # limit_task_cpu_to = 10
    # set_cpu_limit(limit_task_cpu_to, task_pid)

    broadcast_message('status', namespace, 'Begin')
    broadcast_message(task_event, namespace, 'Begin task {}'.format(fibonacci_task.request.id))
    n1, n2 = 0, 1
    count = 0

    # check if the number of terms is valid
    if n <= 0:
        pass
    elif n == 1:
        broadcast_message(task_event, namespace, str(n1))
    else:
        while count < n:
            broadcast_message(task_event, namespace, str(n1)[0:20])
            nth = n1 + n2
            # update values
            n1 = n2
            n2 = nth
            count += 1
    broadcast_message(task_event, namespace, 'End Task {}'.format(fibonacci_task.request.id))
    broadcast_message('status', namespace, 'End')
    applogger.info("end fibonacci_task")
    # cpu_unlimit(task_pid)
    return n1


@celery_app.task
def matrix_task(session, task_event, namespace):

    applogger.info("start matrix_task")
    room = session
    namespace = '/long_task'

    task_pid = os.getpid()
    applogger.info(f'proc matrix index {os.getpid()}')

    limit_task_cpu_to = 10
    # set_cpu_limit(limit_task_cpu_to, task_pid)

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


@celery_app.task
def schedule_task(task_event, namespace):
    # Inspect all nodes.
    i = celery_app.control.inspect()

    # Show tasks that are currently active.
    # i.active()


    # applogger.info(f"start schedule_task {task_event}, {namespace}")
    broadcast_message('status', namespace, 'Begin_schedule_task')
    broadcast_message(task_event, namespace, str(i.active()))
    # broadcast_message(task_event, namespace, 'This task will print 10 random numbers')
    # for i in range(10):
    #     broadcast_message(task_event, namespace, str(random.randint(1, 100000)))
    #     time.sleep(1)
    # broadcast_message(task_event, namespace, 'End Task {}'.format(schedule_task.request.id))
    broadcast_message('status', namespace, 'End')


def exception_func():
    raise ValueError
