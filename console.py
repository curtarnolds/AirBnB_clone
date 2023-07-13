#!/usr/bin/python3
"""A console program containing the entry point of the command interpreter."""
import cmd
from models.base_model import BaseModel  # noqa
from models.engine.file_storage import FileStorage
from models import storage
from models.user import User  # noqa


class HBNBCommand(cmd.Cmd):
    """Defines a command interpreter."""
    prompt = '(hbnb) '
    __cls_list = ['BaseModel', 'User']

    def emptyline(self) -> bool:
        """Override emptyline behaviour."""
        pass

    def do_create(self, line):
        """Create a new instance of BaseModel, saves it and prints the id."""
        argv = line.split()
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
        argv = line.split()
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in [val['__class__']
                             for val in storage.all().values()]:
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
        argv = line.split()
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in [val['__class__']
                             for val in storage.all().values()]:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif f'{argv[0]}.{argv[1]}' not in storage.all().keys():
            print("** no instance found **")
        else:
            FileStorage.delete(f'{argv[0]}.{argv[1]}')
            storage.save()

    def do_all(self, line):
        """Print all string representation of instances based or not on
        the class name.
        """
        argv = line.split()
        if len(argv) > 0:
            if argv[0] not in [val['__class__']
                               for val in storage.all().values()]:
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
        argv = line.split()
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
            strp_val = argv[3].strip('\"\'')
            print(strp_val)
            setattr(tmp, argv[2], strp_val)
            tmp.save()

    def do_quit(self, line):
        """Exits the program."""
        return True

    def do_EOF(self, line):
        """Exits the program."""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
