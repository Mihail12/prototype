import resource
import time

from flask import render_template, request, jsonify, session
from flask_socketio import SocketIO, join_room
import uuid
from random import randint
import tasks
from __init__ import create_app


app = create_app()
app.secret_key = "DataRoadReflect"

applogger = app.logger
socketio = SocketIO(app, message_queue='redis://')

user_1 = {
    'id': 1,
    'name': 'John',
}

user_2 = {
    'id': 1,
    'name': 'John',
}

user_3 = {
    'id': 1,
    'name': 'John',
}


@app.route("/", methods=['GET'])
def index():

    # create a unique session id
    if 'uid' not in session:
        session['uid'] = str(uuid.uuid4())

    return render_template('index.html')


@app.route("/runTask", methods=['POST'])
def long_task_endpoint():
    applogger.info(f"long_task_endpoint touched with request method {request.method}")

    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    n = randint(0, 100)
    sid = str(session['uid'])
    task = tasks.long_task.apply_async((n, sid, task_event, namespace))

    return jsonify({'id': task.id})


@app.route("/run-fibonacci-task", methods=['POST'])
def fibonacci_task_endpoint():
    applogger.info(f"fibonacci_task_endpoint touched with request method {request.method}")
    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    n = randint(10000, 20000)
    sid = str(session['uid'])
    task = tasks.fibonacci_task.delay(n=n, session=sid, task_event=task_event, namespace=namespace)
    return jsonify({'id': task.id})


@app.route("/matrix-task", methods=['POST'])
def matrix_task_endpoint():
    applogger.info(f"matrix_task_endpoint touched with request method {request.method}")
    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    sid = str(session['uid'])
    task = tasks.matrix_task.delay(session=sid, task_event=task_event, namespace=namespace)
    return jsonify({'id': task.id})


@app.route("/api/test", methods=['GET'])
def test_api():

    time.sleep(4)
    variable = randint(1, 10000)

    return jsonify({'variable': variable})


@socketio.on('connect')
def socket_connect(*args, **kwargs):
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
