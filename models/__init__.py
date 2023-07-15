#!/usr/bin/python3
"""__init__ for models package."""
from .engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
