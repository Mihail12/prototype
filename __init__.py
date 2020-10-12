import logging

from celery import Celery
from flask import Flask


def create_app():
    flask_app = Flask(__name__)
    flask_app.secret_key = "Prototype"

    file_handler = logging.FileHandler("info.log")
    auth_file_handler = logging.FileHandler("auth.log")
    file_handler.setLevel(logging.DEBUG)
    auth_file_handler.setLevel(logging.WARNING)

    flask_app.logger.handlers.clear()
    flask_app.logger.addHandler(file_handler)
    flask_app.logger.addHandler(auth_file_handler)
    return flask_app


class CeleryObj:
    celery = None

    def __init__(self, broker):
        self.celery = Celery('demo', broker=broker, include=['tasks'])

    def get_celery(self):
        return self.celery
