import unittest

from shared.range import Range


class TestRange(unittest.TestCase):

    def test_range_given_current_value_only(self):
        _range = Range(5)
        self.assertEqual(_range.current, 5)
        self.assertEqual(_range.max, 5)
        self.assertEqual(_range.min, 5)

    def test_range_given_current_and_max(self):
        _range = Range(5, _max=7)
        self.assertEqual(_range.current, 5)
        self.assertEqual(_range.max, 7)
        self.assertEqual(_range.min, 5)

    def test_range_given_current_and_min(self):
        _range = Range(5, _min=2)
        self.assertEqual(_range.current, 5)
        self.assertEqual(_range.max, 5)
        self.assertEqual(_range.min, 2)

    def test_range_given_current_and_min_and_max(self):
        _range = Range(5, _min=2, _max=7)
        self.assertEqual(_range.current, 5)
        self.assertEqual(_range.max, 7)
        self.assertEqual(_range.min, 2)
