import random
import time

from celery import Celery
from flask import render_template, request, jsonify, session
from flask_socketio import SocketIO, join_room
from random import randint

import celeryconfig
from __init__ import create_app


flask_app = create_app()
flask_app.secret_key = "DataRoadReflect"

celery_app = Celery('demo', broker='redis://localhost:6379', include=['tasks'])
celery_app.config_from_object(celeryconfig)

applogger = flask_app.logger
socketio = SocketIO(flask_app, message_queue='redis://')

user_1 = {
    'id': 1,
    'name': 'John',
    'role': 'manager',
    'age': 60,
}

user_2 = {
    'id': 2,
    'name': 'Bob',
    'role': 'manager',
    'age': 22,
}

user_3 = {
    'id': 3,
    'name': 'Jane',
    'role': 'customer',
    'age': 15,
}
user_4 = {
    'id': 4,
    'name': 'Den',
    'role': 'customer',
    'age': 65,
}
users = [user_1, user_2, user_3, user_4]


@flask_app.route("/", methods=['GET'])
def index():
    current_user = random.choice(users)
    # create a unique session id
    session['uid'] = current_user['id']
    session['user_role'] = current_user['role']
    session['age'] = current_user['age']

    return render_template('index.html', **current_user)


@flask_app.route("/runTask", methods=['POST'])
def long_task_endpoint():
    applogger.info(f"long_task_endpoint touched with request method {request.method}")

    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    n = randint(5, 20)
    task = celery_app.send_task('tasks.long_task', args=(n, task_event, namespace))

    return jsonify({'id': task.id, "number": n})


@flask_app.route("/run-fibonacci-task", methods=['POST'])
def fibonacci_task_endpoint():
    applogger.info(f"fibonacci_task_endpoint touched with request method {request.method}")
    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    n = randint(10000, 20000)
    task = celery_app.send_task('tasks.fibonacci_task', args=(n, task_event, namespace))
    return jsonify({'id': task.id, "number": n})


@flask_app.route("/matrix-task", methods=['POST'])
def matrix_task_endpoint():
    applogger.info(f"matrix_task_endpoint touched with request method {request.method}")
    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    sid = str(session['uid'])
    task = celery_app.send_task('tasks.matrix_task', args=(sid, task_event, namespace))
    return jsonify({'id': task.id})


@flask_app.route("/api/test", methods=['GET'])
def test_api():

    time.sleep(4)
    variable = randint(1, 10000)

    return jsonify({'variable': variable})


@socketio.on('connect', namespace='/managers')
def socket_connect_auth(*args, **kwargs):
    if session['user_role'] != 'manager':
        print('NOT connected')
        raise ConnectionRefusedError('unauthorized!')

    print('connected socket_connect_auth')


@socketio.on('connect', namespace='/aged')
def socket_connect_auth(*args, **kwargs):
    if int(session['age']) < 60:
        print('NOT connected')
        raise ConnectionRefusedError('unauthorized!')

    print('connected socket_connect_auth')


@socketio.on('connect')
def socket_auth(*args, **kwargs):
    # user = request.user
    # if user.is_authenticated():
    #     return 'Not Allowed'

    user_data = args
    print('connected socket_auth')
    # your logic ...
    # app.login(user_data)


@socketio.on('join_room', namespace='/long_task')
def on_room(*args, **kwargs):

    room = str(session['uid'])

    print('join room {}'.format(room))

    join_room(room)


@socketio.on('join_room', namespace='/schedule_task')
def on_room(*args, **kwargs):
    print('connected schedule_task')

if __name__ == "__main__":

    import logging
    logging.basicConfig(filename='error.log', level=logging.DEBUG)

    socketio.run(flask_app, debug=True, host="0.0.0.0")
