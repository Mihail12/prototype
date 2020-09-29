import numpy
from celery import Celery
import time
from flask_socketio import SocketIO
from numpy import argsort

celery = Celery('demo', broker='redis://localhost:6379')

socketio = SocketIO(message_queue='redis://')


def send_message(event, namespace, room, message):
    print(message)
    socketio.emit(event, {'msg': message}, namespace=namespace, room=room)


@celery.task
def long_task(n, session, task_event, namespace):
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


@celery.task
def fibonacci_task(n, session, task_event, namespace):
    room = session
    namespace = '/long_task'

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


@celery.task
def matrix_task(session, task_event, namespace):

    room = session
    namespace = '/long_task'

    send_message('status', namespace, room, 'Begin')
    send_message(task_event, namespace, room, 'Begin task {}'.format(matrix_task.request.id))

    a = numpy.random.rand(100000, 100)
    b = numpy.random.rand(300000, 100)
    c = numpy.dot(b, a.T)
    send_message(task_event, namespace, room, 'Matrices doted')

    send_message(task_event, namespace, room, 'Matrix sorting....')
    sorted = [argsort(j)[:10] for j in c.T]
    print(sorted)
    send_message(task_event, namespace, room, 'Matrix sorted')

    send_message(task_event, namespace, room, 'End Task {}'.format(matrix_task.request.id))
    send_message('status', namespace, room, 'End')
