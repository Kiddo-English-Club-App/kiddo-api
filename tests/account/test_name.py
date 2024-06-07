import unittest
from shared.name import NameStr
from shared import exceptions


class TestName(unittest.TestCase):

    def test_name_equality(self):
        name = NameStr("John")
        self.assertEqual(name, "John")

    def test_name_length_validation(self):
        with self.assertRaisesRegex(exceptions.ValidationError, "(.)*2 characters(.)*"):
            NameStr("J")
    
    def test_name_with_digits(self):
        with self.assertRaisesRegex(exceptions.ValidationError, "(.)*alphabetic(.)*"):
            NameStr("John1")

    def test_name_with_special_character(self):
        with self.assertRaisesRegex(exceptions.ValidationError, "(.)*alphabetic(.)*"):
            NameStr("John@")
    
    def test_name_title_cased(self):
        with self.assertRaisesRegex(exceptions.ValidationError, "(.)*title cased(.)*"):
            NameStr("john")
    
    def test_name_strip(self):
        name = NameStr(" John ")
        self.assertEqual(name, "John")
