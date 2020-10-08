import os
import sys
from unittest.mock import patch, Mock


from .base import BaseTests
# This row of code should be in order to start test without error.
# This row should be below import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tasks import long_task, fibonacci_task, exception_func


def fib(term):
    if term <= 1:
        return (term)
    return (fib(term-1) + fib(term-2))


class TasksTestCase(BaseTests):
    @classmethod
    def setUpClass(cls):
        super(TasksTestCase, cls).setUpClass()

    @patch('tasks.applogger')
    @patch('tasks.broadcast_message')
    @patch('time.sleep')
    def test_long_task(self, _, __, ___):
        result = long_task(10, 'task_event', 'namespace')
        self.assertEqual(result, 'Done')

    @patch('tasks.applogger')
    @patch('tasks.broadcast_message')
    def test_fibonacci_task(self, _, __):
        result = fibonacci_task(10, 'task_event', 'namespace')
        self.assertEqual(result, fib(10))

    def test_exception_task(self):
        with self.assertRaises(ValueError):
            exception_func()
