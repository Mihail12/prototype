import logging

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
