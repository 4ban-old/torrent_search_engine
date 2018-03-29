# -*- coding: utf-8 -*-
"""
    Commands list.
"""


class Commands:
    def __init__(self):
        self.prefix = '_sh_'
    
    def get_command(self, command):
        return getattr(self, self.prefix+command, None)

    def get_all_commands(self):
        commands = list()
        for m in dir(self):
            name = m[len(self.prefix):]
            command = self.get_command(name)
            if command is not None:
                commands.append((name, command))
        return commands

    def _sh_help(self, attr=None):
        """
        Help for help
        """
        attr = getattr(self, self.prefix+attr, None)
        if attr is None:
            print 'This function doesn\'t exist!'
        else:
            print attr.__doc__

    def _sh_hello(self, *args):
        """
        11111 Help for function hello
        """
        print 'hello world1111'


class Commands2:
    def __init__(self):
        self.prefix = '_sh_'

    def get_command(self, command):
        return getattr(self, self.prefix+command, None)

    def get_all_commands(self):
        commands = list()
        for m in dir(self):
            name = m[len(self.prefix):]
            command = self.get_command(name)
            if command is not None:
                commands.append((name, command))
        return commands

    def _sh_hello(self, *args):
        """
        22222 Help for function hello
        """
        print 'hello world22222'

