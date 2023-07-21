#!/usr/bin/python3
"""A console program containing the entry point of the command interpreter."""
from models.base_model import BaseModel  # noqa
from models.user import User  # noqa
from models.amenity import Amenity  # noqa
from models.city import City  # noqa
from models.place import Place  # noqa
from models.review import Review  # noqa
from models.state import State  # noqa
from models import storage
import re
import cmd


def to_list(argv: str) -> list:
    """Convert a string to a list."""
    return [item.strip('"') for item in re.findall(r'"[^"]+"|\b\w+\b', argv)]


def validate_class_name(class_name: str) -> bool:
    """Validate a class name"""
    return class_name in HBNBCommand.cls_list


def check_args(line: str) -> bool:
    """Check the number and kind of arguments passed in interpreter."""
    import inspect
    caller_name = inspect.currentframe().f_back.f_code.co_name
    argv = [item.strip('"')
            for item in re.findall(r'"[^"]+"|\b\w+\b', line) if item]
    if len(argv) < 1:
        print("** class name missing **")
    elif not validate_class_name(argv[0]):
        print("** class doesn't exist **")
    elif len(argv) == 1:
        if caller_name != 'do_create':
            print("** instance id missing **")
        else:
            return argv
    elif f'{argv[0]}.{argv[1]}' not in storage.all().keys():
        print("** no instance found **")
    elif caller_name == "do_update" and len(argv) == 2:
        print("** attribute name missing **")
    elif caller_name == "do_update" and len(argv) == 3:
        print("** value missing **")
    else:
        return argv


class HBNBCommand(cmd.Cmd):
    """Defines a command interpreter."""
    prompt = '(hbnb) '
    cls_list = ['BaseModel', 'User', 'State', 'City', 'Amenity', 'Place',
                'Review']

    def emptyline(self) -> bool:
        """Override emptyline behaviour."""
        pass

    def precmd(self, line: str) -> str:
        """Preprocess command to allow retrieval
        of all instances of a class."""
        argv = re.findall(r'"[^"]+"|\b\w+\b', line)
        # argv = [item.strip('"') for item in re.findall(r'"[^"]+"|\b\w+\b', line)] # noqa
        if len(argv) > 0 and validate_class_name(argv[0]):
            return f"{argv[1]} {argv[0]} {' '.join(argv[2:])}"
        else:
            return super().precmd(line)

    def do_create(self, line: str) -> None:
        """Create a new instance of BaseModel, saves it and prints the id."""
        argv = [item.strip('"') for item in re.split(
            r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line) if item]
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in __class__.cls_list:
            print("** class doesn't exist **")
        else:
            tmp_instance = eval(f"{argv[0]}()")
            storage.save()
            print(tmp_instance.id)

    def do_show(self, line):
        """Print the string representation of an instance based
        on the class name and id.
        """
        argv = [item.strip('"') for item in re.split(
            r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line) if item]
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in __class__.cls_list:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif f'{argv[0]}.{argv[1]}' not in storage.all().keys():
            print("** no instance found **")
        else:
            objs = storage.all()
            obj_key = f"{argv[0]}.{argv[1]}"
            obj = objs[obj_key]
            tmp = eval(f"{argv[0]}(**{obj.to_dict()})")
            print(tmp)

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id."""
        argv = [item.strip('"') for item in re.split(
            r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line) if item]
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in __class__.cls_list:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif f'{argv[0]}.{argv[1]}' not in storage.all().keys():
            print("** no instance found **")
        else:
            storage.delete(f'{argv[0]}.{argv[1]}')
            storage.save()

    def do_all(self, line):
        """Print all string representation of instances based or not on
        the class name.
        """
        argv = [item.strip('"') for item in re.split(
            r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line) if item]

        if len(argv) > 0:
            if argv[0] not in __class__.cls_list:
                print("** class doesn't exist **")
            else:
                print([str(value) for value
                       in storage.all().values() if value.__class__.__name__ ==
                       argv[0]])
        else:
            print([str(value) for
                   value in storage.all().values()])

    def do_update(self, line):
        """Update an instance based on the class name and id by adding or
        updating attribute.
        """
        argv = [item.strip('"') for item in re.split(
            r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line) if item]

        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in __class__.cls_list:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif f'{argv[0]}.{argv[1]}' not in storage.all().keys():
            print("** no instance found **")
        elif len(argv) == 2:
            print("** attribute name missing **")
        elif len(argv) == 3:
            print("** value missing **")
        else:
            objs = storage.all()
            obj_key = f"{argv[0]}.{argv[1]}"
            if obj_key in objs.keys():
                obj = objs[obj_key]
                try:
                    _idx = 0
                    while argv[2 + _idx] and argv[3 + _idx]:
                        setattr(obj, argv[2 + _idx], argv[3 + _idx])
                        _idx = _idx + 2
                    obj.save()
                except IndexError:
                    pass
            else:
                print("** no instance found **")

    def do_count(self, line):
        """Retrieve the number of instances of a class."""
        argv = [item.strip('"') for item in re.split(
            r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line) if item]
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in __class__.cls_list:
            print("** class doesn't exist **")
        else:
            print(len([obj for obj in storage.all().values()
                       if obj.__class__.__name__ == argv[0]]))

    def do_quit(self, line):
        """Exits the program."""
        return True

    def do_EOF(self, line):
        """Exits the program."""
        return True

    def help_quit(self):
        print('\n'.join([
            'Usage:',
            "\tquit"
        ]))

    def help_EOF(self):
        print('\n'.join([
            'Usage:',
            "\tWindows/Linux: Ctrl+D",
            "\tMac: Cmd+D"
        ]))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
