import os
import sys
from unittest import TestCase
from unittest.mock import patch


# This row of code should be in order to start test without error.
# This row should be below import from app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
with patch('__init__.logging') as mock:
    from f_app import flask_app


class BaseTests(TestCase):

    ############################
    #### setup and teardown ####
    ############################

    @classmethod
    def setUpClass(cls):
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
        flask_app.config['DEBUG'] = False
        flask_app.config['BASEDIR'] = os.getcwd()
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        #                                         os.path.join(app.config['BASEDIR'], TEST_DB)
        cls.client = flask_app.test_client()
