# -*- coding: utf-8 -*-
"""
    Shell
"""
__author__ = 'Dmitry Kryukov'

import collections
import os
import random
import types

from importlib import import_module
from base64 import b64decode
from bz2 import decompress

from cprint import cprint


ParsedCommand = collections.namedtuple('ParsedCommand', ('set', 'command', 'args',), verbose=False)
ParsedArgs = collections.namedtuple('ParsedArgs', ('args', 'sets', 'names'), verbose=False)


def _parse_command(cmd):
    """ Parse command string into named tuple """
    cmd = cmd.strip(' ')
    cls = ''
    if cmd.startswith('$'):
        cls, cmd = cmd.split(' ', 1)
        cls = cls[1:]
        cmd = cmd.strip(' ')
    cmd += ' '
    cmd, attr = cmd.split(' ', 1)
    attr = attr.strip(' ')
    return ParsedCommand(cls, cmd, attr)

def _parse_args(args):
    args = args.strip(' ')
    args = args.split(' ')
    arguments = ''
    sets = list()
    names = list()
    for a in args:
        a = a.strip(' ')
        if not a: continue
        if a.startswith('$'):
            sets.append(a[1:])
        elif a.startswith('-'):
            arguments += a[1:]
        else:
            names.append(a)
    return ParsedArgs(arguments, sets, names)


class BuiltInCommands(object):
    def __init__(self):
        self.exit = False
        self.commands_sets = dict()

    def get_command(self, command):
        return getattr(self, '_shell_'+command, None)

    def get_all_commands(self):
        commands = list()
        for m in dir(self):
            name = m[7:]
            command = self.get_command(name)
            if command is not None:
                commands.append((name, command))
        return commands

    # EXIT
    def _shell_exit(self, *args):
        self.exit = True
    def _shell_quit(self, *args):
        self._shell_exit()
    def _shell_bye(self, *args):
        self._shell_exit()

    # help
    def _shell_help(self, args=None):
        """
            Command `help` shows documentation of command
            
            help [$set] -a [command1 [command2]...]
            
            if [$set], `help` will look
            for function and its documentation in
            designated set. If not, `help` will
            search function in build-in commands.

            -a - mean all. `help` will search
               function and documentation in all
               sets. `-a` can't be used without
               [command]

            -l - mean list. `help` will search
               function in all sets and shows
               a list of sets. `-l` can be used
               without [command] to show all
               commands in all sets

            help with no command shows a list of
            built-in commands.
        """
        if args is None:
            args = ''
        args = _parse_args(args)
        if not (args.args or args.sets or args.names):
            args = _parse_args('-l')
        known_args = 'al'
        wrong = False
        if len(args.args) > 1:
            cprint('[red]Wrong arguments number[/]', colorize=colorize)
            wrong = True
        if args.args not in known_args:
            cprint('[red]Unkown argument[/] [purple]`-%s`[/]' % args.args, colorize=colorize)
            wrong = True
        if args.args == 'a' and not args.names:
            cprint('[yellow]Argument [purple]`-a`[/] cant be used without command[/]', colorize=colorize)
            wrong = True
        if wrong:
            cprint('Try [blue]`help help`[/] for more information', colorize=colorize)
            return

        result = list()
        
        if not args.sets and args.names:
            for name in args.names:
                res = self.get_command(name)
                if res is not None:
                    result.append(('built-in',  name, res.__doc__))
                if args.args:
                    for set_name, set_self in self.commands_sets.items():
                        res = set_self.get_command(name)
                        if res is not None:
                            result.append((set_name, name, res.__doc__))
            if not result:
                cprint('[red]No such command [blue]`%s`[/] in [yellow]built-in[/] functions[/]', colorize=colorize)
                cprint('Try [blue]`help -l [command]`[/] or [blue]`help -a [command]`[/]', colorize=colorize)

        elif args.sets:
            if args.names:
                for set_name, set_self in self.commands_sets.items():
                    if set_name in args.sets:
                        for name in args.names:
                            res = set_self.get_command(name)
                            if res is not None:
                                result.append((set_name, name,  res.__doc__))
            else:
                for set_name in args.sets:
                    if set_name in self.commands_sets:
                        res = self.commands_sets[set_name].get_all_commands()
                        for r in res:
                            result.append('$'+set_name, r[0], r[1].__doc__)
        else:
            res = self.get_all_commands()
            for r in res:
                result.append(('built-in', r[0], r[1].__doc__))
            for set_name, set_self in self.commands_sets.items():
                res = self.commands_sets[set_name].get_all_commands()
                for r in res:
                    result.append((set_name, r[0], r[1].__doc__))
        if args.args == 'a':
            result = sorted(result, key=lambda x: x[0])
            set_name = ''
            for res in result:
                if set_name != res[0]:
                    set_name = res[0]
                    cprint('\n  [green]$%s[/]' %set_name, colorize=colorize)
                cprint(res[2], colorize=colorize)
        elif args.args == 'l':
            if args.names:
                result = sorted(result, key=lambda x: x[1])
                command_name = ''
                for res in result:
                    if command_name != res[1]:
                        command_name = res[1]
                        cprint('\n Command [blue]`%s`[/] found in:' % command_name, colorize=colorize)
                    cprint('[yellow]$%s[/]' % res[0], colorize=colorize)
            else:
                result = sorted(result, key=lambda x: x[0])
                set_name = ''
                for res in result:
                    if set_name != res[0]:
                        set_name = res[0]
                        cprint('\n  [yellow]$%s[/]' %set_name, colorize=colorize)
                    cprint('[blue]'+res[1]+'[/]', colorize=colorize)

        else:
            for res in result:
                cprint('[yellow]$%s[/] -> [blue]%s[/]' % (res[0], res[1]), colorize=colorize)
                cprint(res[2], colorize=colorize)

    # register set
    def _shell_reg(self, args):
        """
            Command `reg` allow to control registered sets

            reg -ldr [set_name] [new_set_name]
                l - show list of registered sets
                d - delete set
                r - register set
                u - unregister (same as -d)
        """

        args = _parse_args(args)
        wrong = False
        known_args = 'ldru'

        if args.args and args.args not in known_args:
            cprint('[red]Unknown arguments[/]', colorize=colorize)
            wrong = True

        if wrong:
            cprint('Try [blue]`help reg`[/] for more information', colorize=colorize)
            return

        if args.args == 'l':
            for set_name in self.commands_sets:
                cprint('[yellow]$%s[/]' % set_name, colorize=colorize)
        for arg in args.args:
            if arg == 'r':
                name = ''
            if not args.names:
                cprint('What must I registrate?', colorize=colorize)
                return
            for name in names:
                m = import_module(mod)


class Shell(BuiltInCommands):
    def __init__(self, asciiart=False):
        super(Shell, self).__init__()
        self.commands_sets = dict()
        self.asciiart = list()
        if asciiart and os.path.exists('ASCII.art'):
            with open('ASCII.art') as f:
                asciiart = f.read()
                asciiart = asciiart.split('\n\n')
                asciiart = filter(lambda x:  bool(x.replace('\n', '')), asciiart)
            self.asciiart = asciiart[:]

        if not self.asciiart:
            art = ('QlpoOTFBWSZTWYNxiDsAABj/gH/6oABg54AaJMHMJMJElCQwATikETCQZDRBoZ'
                   'PKepoaGCDAyDIADEaDIZAYNMhIyJtUB6TRkANDQLjX3QA2niQGG7WaLiN67d88'
                   'jqcO7D8zYMzAY1gZZvFQhVRAoNmQgtJAJAEnhAVKwqhS5Fbd5ElGYSIwIQwTXL'
                   'UhffKeMDK1U4xIsdKfr+0bAbPJkM9qxMKFkoDQlTHHeUUg+YXpZg8HQFt4yJKF'
                   'dJRKw8IpHm+lkOcrbbpNCNCwsxMEFiFzJSoTuTcgIZwHNbIlnEiru5xdAgp7RD'
                   'cMr7r9f9SLtFi+HViIytruno6KAC4Wk192MgZZaapqOuk7+S1OdCtLSUQXl2wR'
                   'YpmZCACYxqX3mfh5lp3ECSsagyDF5HotvgrVyTpUR8VIO2ecdjPaH1n4bK8f4u'
                   '5IpwoSEG4xB2A=')
            self.asciiart.append(decompress(b64decode(art)))
        self.line = 'hypno-shell# '
        self.reserved_commands = ['help', 'reg']

    def register(self, cls):
        """
            Add set of commands
            Added set is a class, with `get_command` method
        """

        # Use instances, not classes
        if isinstance(cls, (type, types.ClassType)):
            cls = cls()
        # Check `get_command` exists
        tmp = cls.get_command('command')
        # Name dublicates must be changed
        # as 'name_N' where N is number
        cname = cls.__class__.__name__
        changed_name = cname
        count = -1
        while changed_name:
            count += 1
            changed_name = cname + '_' + str(count) if count else changed_name
            if changed_name not in self.commands_sets:
                self.commands_sets[changed_name] = cls
                changed_name = ''

    def unregister(self, set_name=None):
        if set_name is None:
            self.commands_sets = dict()
        else:
            try:
                del self.commands_sets[set_name]
            except KeyError:
                # TODO: Find same names with added numbers
                cprint('[red]Commands set [yellow]`%s`[/] does not exist.[/]' % set_name, colorize=colorize)
                cprint('Use [blue]`reg -l`[/] for list of registered sets', colorize=colorize)

    def run(self, unreg=True):
        print random.choice(self.asciiart)
        print '\n\n'
        cprint('\n[cyan][underline]Hypno-Shell. version 0.1[/][/]\n', colorize=colorize)
        if not self.commands_sets:
            cprint('[red]No registered commands[/]', colorize=colorize)
            cprint('To register set of commands use[blue] `reg`[/]', colorize=colorize)
            cprint('[blue]`help reg`[/] for more information\n', colorize=colorize)

        # cmd = ''
        while not self.exit:
            try:
                cmd = raw_input(cprint('[green]'+self.line+'[/]', colorize=colorize, noprint=True))
            except KeyboardInterrupt:
                cprint('\nPlease, enter [blue]`exit`[/] or [blue]`quit`[/]', colorize=colorize)
                continue
            # Empty
            if not cmd:
                continue

            parsed_cmd = _parse_command(cmd)
            
            commands = list()
            if parsed_cmd.set:
                if parsed_cmd.set in self.commands_sets:
                    commands.append(self.commands_sets[parsed_cmd.set].get_command(parsed_cmd.command))
                else:
                    cprint('[red]Cant find [blue]`%s`[/] in set [yellow]"%s"[/][/]' % (parsed_cmd.command, parsed_cmd.set), colorize=colorize)
            elif parsed_cmd.command in self.reserved_commands:
                commands.append(self.get_command(parsed_cmd.command))
            else:
                commands.append(self.get_command(parsed_cmd.command))
                for set_name, set_self in self.commands_sets.items():
                    commands.append(set_self.get_command(parsed_cmd.command))
            commands = filter(lambda x: x is not None, commands)

            if commands:
                if len(commands) > 1:
                    cprint('Found [blue]%s[/] commands. Use one from list below:' % len(commands), colorize=colorize)
                    for command in commands:
                        cprint('[yellow]$%s[/] [red]->[/] [blue]%s[/]' % (command.im_class.__name__, parsed_cmd.command), colorize=colorize)
                else:
                    commands[0](parsed_cmd.args) if parsed_cmd.args else commands[0]()
            else:
                cprint('[red]Command [blue]`%s`[/] does not exists![/]' % parsed_cmd.command, colorize=colorize)
        if unreg:
            self.unregister()


if __name__ == '__main__':
    s = Shell()
    colorize = False
    #from pudge_commands import PudgeCommands
    #s.register(PudgeCommands)
    from commands import *
    s.register(Commands)
    s.register(Commands2)
    s.run()
