import importlib
import sys
import unittest
from datetime import datetime, time

from main import Model


class TestModel(unittest.TestCase):
    def test_is_between_in_one_day(self):
        now = time(5)
        start = time(0)
        end = time(7)
        model = Model(start, end)
        self.assertTrue(model.is_between(now, start, end))
        now = time(11)
        self.assertFalse(model.is_between(now, start, end))

    def test_is_between_cross_midnight(self):
        now = time(0)
        start = time(11)
        end = time(4)
        model = Model(start, end)
        self.assertTrue(model.is_between(now, start, end))


if __name__ == "__main__":
    unittest.main()
