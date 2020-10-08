import os
import sys
from unittest import TestCase

# This row of code should be in order to start test without error.
# This row should be below import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


class BaseTests(TestCase):

    ############################
    #### setup and teardown ####
    ############################

    @classmethod
    def setUpClass(cls):
        # app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['BASEDIR'] = os.getcwd()
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        #                                         os.path.join(app.config['BASEDIR'], TEST_DB)
        cls.client = app.test_client()
        # pdb.set_trace()
        # type here the data that should be created one along this class test
        # pdb.set_trace()