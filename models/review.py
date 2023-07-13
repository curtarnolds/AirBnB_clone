#!/usr/bin/python3
"""Defines a review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """A Review class."""
    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
