#!/usr/bin/python3
"""Test suite for the User class in models.user"""
import unittest
from models.base_model import BaseModel

from models.user import User


class TestUser(unittest.TestCase):
    """Test cases against the User class"""

    def test_attrs_are_class_attrs(self):
        """Check if attributes are class attributes."""
        u = User() # noqa
        # test that it is a class attribute
        self.assertTrue(hasattr(User, "first_name")
                        and hasattr(User, "last_name"))

    def test_class_attrs(self):
        """Check if the class attributes are assigned their default values."""
        u = User()
        self.assertIs(type(u.first_name), str)
        self.assertIs(type(u.last_name), str)
        self.assertTrue(u.first_name == "")
        self.assertTrue(u.last_name == "")

    def test_user_is_a_subclass_of_basemodel(self):
        """Check if User is a subclass of BaseModel."""
        u = User()
        self.assertTrue(issubclass(type(u), BaseModel))
