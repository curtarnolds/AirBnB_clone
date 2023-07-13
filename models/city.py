#!/usr/bin/python3
"""Defines a city class."""
from models.base_model import BaseModel


class City(BaseModel):
    """A City class."""
    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a City instance."""
        super().__init__(*args, **kwargs)
