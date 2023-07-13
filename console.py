#!/usr/bin/python3
"""A console program containing the entry point of the command interpreter."""
import cmd
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage


class HBNBCommand(cmd.Cmd):
    """Defines a command interpreter."""
    prompt = '(hbnb) '

    def emptyline(self) -> bool:
        """Override emptyline behaviour."""
        pass

    def do_create(self, line):
        """Create a new instance of BaseModel, saves it and prints the id."""
        if not line:
            print("** class name missing **")
        elif line != 'BaseModel':
            print("** class doesn't exist **")
        else:
            tmp_model = BaseModel()
            print(tmp_model.id)

    def do_show(self, line):
        """Print the string representation of an instance based
        on the class name and id.
        """
        argv = line.split()
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in [val['__class__']
                             for val in FileStorage.all(self).values()]:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif f'{argv[0]}.{argv[1]}' not in FileStorage.all(self).keys():
            print("** no instance found **")
        else:
            print(BaseModel(**FileStorage.all(self)[
                f'{argv[0]}.{argv[1]}']))

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id."""
        argv = line.split()
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in [val['__class__']
                             for val in FileStorage.all(self).values()]:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif f'{argv[0]}.{argv[1]}' not in FileStorage.all(self).keys():
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
                               for val in FileStorage.all(self).values()]:
                print("** class doesn't exist **")
            else:
                print([str(eval(f'{argv[0]}(**{value})')) for value in
                       FileStorage.all(self).values() if value['__class__'] ==
                       argv[0]])
        else:
            print([str(eval(f"{value['__class__']}(**{value})")) for value
                   in FileStorage.all(self).values()])

    def do_update(self, line):
        """Update an instance based on the class name and id by adding or
        updating attribute.
        """
        argv = line.split()
        if len(argv) < 1:
            print("** class name missing **")
        elif argv[0] not in [val['__class__']
                             for val in FileStorage.all(self).values()]:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif f'{argv[0]}.{argv[1]}' not in FileStorage.all(self).keys():
            print("** no instance found **")
        elif len(argv) == 2:
            print("** attribute name missing **")
        elif len(argv) == 3:
            print("** value missing **")
        else:
            objs = FileStorage.all(self)
            obj_key = f"{argv[0]}.{argv[1]}"
            if obj_key not in objs.keys():
                print("** no instance found **")
                return

            obj = objs[obj_key]
            tmp = eval(f"{argv[0]}(**{obj})")
            setattr(tmp, argv[2], argv[3].strip('\"'))
            tmp.save()

    def do_quit(self, line):
        """Exits the program."""
        return True

    def do_EOF(self, line):
        """Exits the program."""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
