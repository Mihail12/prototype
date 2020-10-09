import random
import time

from celery import Celery
from flask import render_template, request, jsonify, session
from flask_socketio import SocketIO, join_room
from random import randint
from __init__ import create_app, CeleryObj

app = create_app()
app.secret_key = "DataRoadReflect"

celery = Celery('demo', broker=['pyamqp://guest@localhost//', 'redis://localhost:6379'], include=['tasks', 'task1'])

applogger = app.logger
socketio = SocketIO(app, message_queue='redis://')

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


@app.route("/", methods=['GET'])
def index():
    current_user = random.choice(users)
    # create a unique session id
    session['uid'] = current_user['id']
    session['user_role'] = current_user['role']
    session['age'] = current_user['age']

    return render_template('index.html', **current_user)


@app.route("/runTask", methods=['POST'])
def long_task_endpoint():
    applogger.info(f"long_task_endpoint touched with request method {request.method}")

    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    n = randint(5, 20)
    task = celery.send_task('tasks.long_task', args=(n, task_event, namespace))

    return jsonify({'id': task.id, "number": n})


@app.route("/run-fibonacci-task", methods=['POST'])
def fibonacci_task_endpoint():
    applogger.info(f"fibonacci_task_endpoint touched with request method {request.method}")
    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    n = randint(10000, 20000)
    task = celery.send_task('tasks.fibonacci_task', args=(n, task_event, namespace))
    return jsonify({'id': task.id, "number": n})


@app.route("/matrix-task", methods=['POST'])
def matrix_task_endpoint():
    applogger.info(f"matrix_task_endpoint touched with request method {request.method}")
    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    sid = str(session['uid'])
    task = celery.send_task('tasks.matrix_task', args=(sid, task_event, namespace))
    return jsonify({'id': task.id})


@app.route("/run-not-auth-task", methods=['POST'])
def not_auth_long_task_endpoint():
    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    n = randint(0, 15)
    task = celery.send_task('tasks.not_auth_long_task', args=(n, task_event, namespace))

    return jsonify({'id': task.id})


@app.route("/api/test", methods=['GET'])
def test_api():

    time.sleep(4)
    variable = randint(1, 10000)

    return jsonify({'variable': variable})


@socketio.on('connect', namespace='/managers')
def socket_connect_auth(*args, **kwargs):
    if session['user_role'] != 'manager':
        print('NOT connected')
        raise ConnectionRefusedError('unauthorized!')

    print('connected')


@socketio.on('connect', namespace='/aged')
def socket_connect_auth(*args, **kwargs):
    if int(session['age']) < 60:
        print('NOT connected')
        raise ConnectionRefusedError('unauthorized!')

    print('connected')


@socketio.on('connect')
def socket_connect(*args, **kwargs):
    # user = request.user
    # if user.is_authenticated():
    #     return 'Not Allowed'

    user_data = args
    print('connected')
    # your logic ...
    # app.login(user_data)


@socketio.on('join_room', namespace='/long_task')
def on_room(*args, **kwargs):

    room = str(session['uid'])

    print('join room {}'.format(room))

    join_room(room)


if __name__ == "__main__":

    import logging
    logging.basicConfig(filename='error.log', level=logging.DEBUG)

    socketio.run(app, debug=True, host="0.0.0.0")
