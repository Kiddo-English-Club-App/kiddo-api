import unittest
from uuid import uuid4
from shared.id import Id


class TestId(unittest.TestCase):
    def test_equals(self):
        uuid = uuid4()
        _id = Id(uuid)
        _id2 = Id(uuid)

        self.assertEqual(_id, _id2)
        self.assertNotEqual(_id, Id(uuid4()))

    def test_initialization(self):
        _id = Id(uuid4())
        _id2 = Id(str(uuid4()))
        _id3 = Id()

        self.assertNotEqual(_id, _id2)
        self.assertNotEqual(_id, _id3)
        self.assertNotEqual(_id2, _id3)



