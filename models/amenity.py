#!/usr/bin/python3
"""Defines an amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """An Amenity class."""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initialize an Amenity instance."""
        super().__init__(*args, **kwargs)
