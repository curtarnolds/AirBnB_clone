#!/usr/bin/python3
"""A base_model module to define parent class of all other classes.
"""
import uuid
import datetime
from models import storage


class BaseModel:
    """Defines common attributes/methods of other classes."""
    def __init__(self, *args, **kwargs) -> None:
        """Initialize a BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key in ('created_at', 'updated_at'):
                    value = datetime.datetime.strptime(
                        value, '%Y-%m-%dT%H:%M:%S.%f')
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at
            storage.new(self)
            storage.save()

    def __str__(self) -> str:
        """Return the string representation of the BaseModel instance."""
        return f'[{self.__class__.__name__}] ({self.id}) <{self.__dict__}>'

    def save(self) -> None:
        """Log the time BaseModel instance was updated."""
        self.updated_at = datetime.datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self) -> dict:
        """Return a dictionary representation of the BaseModel instance."""
        tmp_dict = {'__class__': self.__class__.__name__}
        for k, v in self.__dict__.items():
            if k in ('created_at', 'updated_at'):
                v = v.isoformat()
            tmp_dict[k] = v
        return tmp_dict
