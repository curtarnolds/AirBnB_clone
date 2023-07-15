#!/usr/bin/python3
"""Contains the FileStorage class definition."""
import json

from models.base_model import BaseModel  # noqa
from models.user import User  # noqa
from models.amenity import Amenity  # noqa
from models.city import City  # noqa
from models.place import Place  # noqa
from models.review import Review  # noqa
from models.state import State  # noqa


class FileStorage:
    """Defines a FileStorage class."""
    __file_path = 'file.json'
    __objects = {}

    def __init__(self) -> None:
        """Initialize an instance of FileStorage."""
        pass

    def all(self) -> dict:
        """Returns dictionary of all objects."""
        return self.__objects

    def new(self, obj) -> None:
        """Sets in `__objects` the `obj` with key `<obj class name>.id`"""
        self.__objects[
            f'{obj.__class__.__name__}.{obj.id}'] = obj
        print(self.__objects)

    def save(self) -> None:
        """Serialize `__objects` to JSON file specified in `__file_path`."""
        with open(__class__.__file_path, 'w') as json_file:
            tmp_storage = {}
            for key, value in self.__objects.items():
                tmp_storage[key] = value.to_dict()
            json.dump(tmp_storage, json_file)
            print(tmp_storage)

    def reload(self) -> None:
        """Deserialize JSON file specified in `__file_path` to `__objects`"""
        try:
            with open(self.__file_path) as json_file:
                for key, value in json.load(json_file).items():
                    tmp_obj = eval(f'{value["__class__"]}(**{value})')
                    self.__objects[key] = tmp_obj
        except Exception:
            pass

    def delete(cls, key):
        """Deletes key from __objects."""
        __class__.__objects.pop(key)
