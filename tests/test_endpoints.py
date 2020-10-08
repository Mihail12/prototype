from unittest.mock import patch, Mock

from .base import BaseTests


class EndpointsTestCase(BaseTests):
    @classmethod
    def setUpClass(cls):
        super(EndpointsTestCase, cls).setUpClass()

    @patch('app.applogger')
    @patch('app.celery.send_task', return_value=Mock(id='long_id'))
    def test_long_task_200(self, _, send_task_mock):
        response = self.client.post('/runTask')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 'long_id')
        self.assertTrue(response.json['number'] < 100)
        self.assertTrue(response.json['number'] >= 5)

    @patch('app.applogger')
    @patch('app.celery.send_task', return_value=Mock(id='fibonacci_id'))
    def test_fibonacci_task_200(self, _, send_task_mock):
        response = self.client.post('/run-fibonacci-task')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 'fibonacci_id')
        self.assertTrue(response.json['number'] < 20000)
        self.assertTrue(response.json['number'] > 10000)
