import logging

from flask import Flask


def create_app():
    flask_app = Flask(__name__)
    flask_app.secret_key = "Prototype"

    file_handler = logging.FileHandler("info.log")
    file_handler.setLevel(logging.DEBUG)

    flask_app.logger.setLevel(logging.DEBUG)
    flask_app.logger.handlers.clear()
    flask_app.logger.addHandler(file_handler)
    return flask_app