#!/usr/bin/python3
"""Defines a state class."""
from models.base_model import BaseModel


class State(BaseModel):
    """A State class."""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a State instance."""
        super().__init__(*args, **kwargs)
