#!/usr/bin/python3
"""Defines a User class for HBNB users."""
from models.base_model import BaseModel


class User(BaseModel):
    """A User class."""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a User instance."""
        super().__init__(*args, **kwargs)
