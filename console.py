#!/usr/bin/python3
"""A console program containing the entry point of the command interpreter."""
import cmd


class HBNBCommand(cmd.Cmd):
    """Defines a command interpreter."""
    prompt = '(hbnb) '

    def emptyline(self) -> bool:
        """Override emptyline behaviour."""
        pass

    def do_quit(self, line):
        """Exits the program."""
        return True

    def do_EOF(self, line):
        """Exits the program."""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
