#!/usr/bin/python3
"""Contains the FileStorage class definition."""
import json


class FileStorage:
    """Defines a FileStorage class."""
    __file_path = 'file.json'
    __objects = {}

    def __init__(self) -> None:
        """Initialize an instance of FileStorage."""
        pass

    def all(self) -> dict:
        """Returns dictionary of all objects."""
        return __class__.__objects

    def new(self, obj) -> None:
        """Sets in `__objects` the `obj` with key `<obj class name>.id`"""
        __class__.__objects[
            f'{obj.__class__.__name__}.{obj.id}'] = obj.to_dict()

    def save(self) -> None:
        """Serialize `__objects` to JSON file specified in `__file_path`."""
        with open(__class__.__file_path, 'w') as json_file:
            json.dump(__class__.__objects, json_file)

    def reload(self) -> None:
        """Deserialize JSON file specified in `__file_path` to `__objects`"""
        try:
            with open(__class__.__file_path) as json_file:
                __class__.__objects = json.load(json_file)
        except FileNotFoundError:
            pass

    def delete(cls, key):
        """Deletes key from __objects."""
        __class__.__objects.pop(key)
