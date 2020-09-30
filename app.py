import resource
import time
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_socketio import SocketIO, join_room
import uuid
from random import randint, random
import tasks


app = Flask(__name__)
app.secret_key = "DataRoadReflect"

socketio = SocketIO(app, message_queue='redis://')


@app.route("/", methods=['GET'])
def index():

    # create a unique session id
    if 'uid' not in session:
        session['uid'] = str(uuid.uuid4())

    return render_template('index.html')


@app.route("/runTask", methods=['POST'])
def long_task_endpoint():
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    save_hard = hard
    resource.setrlimit(resource.RLIMIT_CPU, (10, hard * 0.8))

    print(f'CPU limited = {resource.getrlimit(resource.RLIMIT_CPU)}')

    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    n = randint(0, 100)
    sid = str(session['uid'])
    task = tasks.long_task.apply_async((n, sid, task_event, namespace))


    return jsonify({'id': task.id})


@app.route("/run-fibonacci-task", methods=['POST'])
def fibonacci_task_endpoint():
    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    n = randint(10000, 20000)
    sid = str(session['uid'])
    task = tasks.fibonacci_task.delay(n=n, session=sid, task_event=task_event, namespace=namespace)
    return jsonify({'id': task.id})


@app.route("/matrix-task", methods=['POST'])
def matrix_task_endpoint():
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
def socket_connect():
    pass


@socketio.on('join_room', namespace='/long_task')
def on_room(*args, **kwargs):

    room = str(session['uid'])

    print('join room {}'.format(room))

    join_room(room)


if __name__ == "__main__":

    import logging
    logging.basicConfig(filename='error.log', level=logging.DEBUG)

    socketio.run(app, debug=True, host="0.0.0.0")
