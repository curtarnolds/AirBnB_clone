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


class HBNBCommand(cmd.Cmd):
    """Defines a command interpreter."""
    prompt = '(hbnb)'
    __cls_list = ['BaseModel', 'User', 'State', 'City', 'Amenity', 'Place',
                  'Review']

    def emptyline(self) -> bool:
        """Override emptyline behaviour."""
        pass

    def precmd(self, line: str) -> str:
        """Preprocess command to allow retrieval
        of all instances of a class."""
        argv = re.findall(r'"[^"]+"|\b\w+\b', line)
        if len(argv) > 0 and argv[0] in __class__.__cls_list:
            return f"{argv[1]} {argv[0]} {' '.join(argv[2:])}"
        else:
            return super().precmd(line)

    def do_create(self, line):
        """Create a new instance of BaseModel, saves it and prints the id."""
        argv = [item.strip('"') for item in re.split(
            r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line) if item]
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in __class__.__cls_list:
            print("** class doesn't exist **")
        else:
            tmp_instance = eval(f"{argv[0]}()")
            print(tmp_instance.id)

    def do_show(self, line):
        """Print the string representation of an instance based
        on the class name and id.
        """
        argv = [item.strip('"') for item in re.split(
            r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line) if item]
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in __class__.__cls_list:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif f'{argv[0]}.{argv[1]}' not in storage.all().keys():
            print("** no instance found **")
        else:
            objs = storage.all()
            obj_key = f"{argv[0]}.{argv[1]}"
            obj = objs[obj_key]
            tmp = eval(f"{argv[0]}(**{obj})")
            print(tmp)

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id."""
        argv = [item.strip('"') for item in re.split(
            r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line) if item]
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in __class__.__cls_list:
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
            if argv[0] not in __class__.__cls_list:
                print("** class doesn't exist **")
            else:
                print([str(eval(f'{argv[0]}(**{value})')) for value in
                       storage.all().values() if value['__class__'] ==
                       argv[0]])
        else:
            print([str(eval(f"{value['__class__']}(**{value})")) for value
                   in storage.all().values()])

    def do_update(self, line):
        """Update an instance based on the class name and id by adding or
        updating attribute.
        """
        print(line)
        argv = [item.strip('"') for item in re.split(
            r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line) if item]

        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in [val['__class__']
                             for val in storage.all().values()]:
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
            if obj_key not in objs.keys():
                print("** no instance found **")
                return

            obj = objs[obj_key]
            tmp = eval(f"{argv[0]}(**{obj})")
            try:
                _idx = 0
                while argv[2 + _idx] and argv[3 + _idx]:
                    setattr(tmp, argv[2 + _idx], argv[3 + _idx])
                    _idx = _idx + 2
            except IndexError:
                pass
            tmp.save()

    def do_count(self, line):
        """Retrieve the number of instances of a class."""
        argv = [item.strip('"') for item in re.split(
            r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line) if item]
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in __class__.__cls_list:
            print("** class doesn't exist **")
        else:
            print(len([obj['__class__'] for obj in storage.all().values()
                       if obj['__class__'] == argv[0]]))

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
