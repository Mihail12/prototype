from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_socketio import SocketIO, join_room
import uuid
from random import randint
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
    task_event = request.form.get('task-event')
    namespace = request.form.get('namespace')
    n = randint(0, 100)
    sid = str(session['uid'])
    task = tasks.long_task.delay(n=n, session=sid, task_event=task_event, namespace=namespace)

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


@socketio.on('connect')
def socket_connect():
    pass


@socketio.on('join_room', namespace='/long_task')
def on_room(*args, **kwargs):

    room = str(session['uid'])

    print('join room {}'.format(room))

    join_room(room)


if __name__ == "__main__":

    socketio.run(app, debug=True, host="0.0.0.0")
