# coding: utf-8
"""
    Default commands for service.
"""
__author__ = 'Dmitry Kryukov'

from multiprocessing import Process
from logging import *
import ConfigParser
import os
# default processes
from pudge import pudge
from nibbler import nibbler
from nox import nox


def _read_config(*args, **kwargs):
    config = ConfigParser.ConfigParser()
    fromConfigForFirstStart = list()
    if os.path.exists('./service.cfg'):
        config.read('./service.cfg')
        info('Reading config.')
        raw = config.get('default', 'childs').split(';')
        raw = filter(lambda x: x != '', raw)
        for child in raw:
             child = child.strip().lower()
             inter = child.split(' ', 2)
             fromConfigForFirstStart.append(inter)
    else:
        warning('Config file doesn\'t exist')
    return fromConfigForFirstStart

def help(*args, **kwargs):
    """
        Help for help functions for service.
        Use:
            help        -> display help for service
            help [name] -> display help for name
    """
    ANSWERS = kwargs['ANS']
    ATTR = kwargs['ATTR']
    if ATTR:
        name = globals().get(kwargs['ATTR'], None)
        if name is not None:
            # TODO save into var and adding to global answer for client
            ANSWERS = name.__doc__
            return ANSWERS
    else:
        ANSWERS = """Help for service.
        This is module for controlling communist project:
            Create child processes
            Delete child processes
            Control child processes
        Also listening UNIX socket in parallel and wait commands from client:
            run(module, funcname, attr) -> create child process.
            status([processname])       -> print status about processname
                                            or about all processes.
            exit()                      -> exit initialization, terminate all processes,
                                            stopping listening socket and exit.
            stop([processname])         -> kill processname child process.
            """
        return ANSWERS


def run(firstStart=False, *args, **kwargs):
    """
        Function starting default modules in child processes.
    """
    # Start processes from config in first time
    if firstStart:
        STARTED_PROCESSES = dict()
        fromConfigForFirstStart = _read_config()
        if fromConfigForFirstStart:
            for process in fromConfigForFirstStart:
                # TODO func + attr if attr is True
                STARTED_PROCESSES[process[0]] = Process(target=globals().get(process[1]))
        else:
            debug('Nothing to starting.')

        for name, process in STARTED_PROCESSES.items():
            try:
                process.start()
                info('Started process %s with pid=%s' % (name, process.pid))
            except:
                warning('I can\'t start process %s', name)
        return STARTED_PROCESSES
    else:
        STARTED_PROCESSES = kwargs['SP']
        ANSWERS = kwargs['ANS']
        ATTR = kwargs['ATTR']
        ATTR = ATTR.strip(' ').lower()
        ATTR = ATTR.split(' ', 1)
        modulename = ATTR[0]
        funcname = ATTR[1]
        STARTED_PROCESSES[modulename] = Process(target=globals().get(funcname))
        STARTED_PROCESSES[modulename].start()
        info('Started process %s with pid=%s' % (modulename, STARTED_PROCESSES[modulename].pid))
        ANSWERS = 'Started process %s with pid=%s' % (modulename, STARTED_PROCESSES[modulename].pid)
        return ANSWERS, STARTED_PROCESSES


def status(*args, **kwargs):
    """
        Function logging status about all running processes.
    """
    STARTED_PROCESSES = kwargs['SP']
    ANSWERS = kwargs['ANS']
    ATTR = kwargs['ATTR']
    # TODO what to do if attr not one? like name name
    if ATTR:
        if ATTR in STARTED_PROCESSES:
            if STARTED_PROCESSES[ATTR].is_alive():
                ANSWERS = 'Process %s with pid=%s is -> OK\n' % (ATTR, STARTED_PROCESSES[ATTR].pid)
            else:
                ANSWERS = 'Process %s is -> DOWN\n' % ATTR
        else:
            ANSWERS = 'No such process with this name. \n'
            ANSWERS += 'All started processes: \n'
            for name in STARTED_PROCESSES.keys():
                ANSWERS += '    -> %s \n' % name
    else:
        for name, process in STARTED_PROCESSES.items():
            if process.is_alive():
                ANSWERS += 'Process %s with pid=%s is -> OK \n' % (name, process.pid)
            else:
                ANSWERS += 'Process %s is -> DOWN' % name
                warning('Process %s is -> DOWN' % name)
    return ANSWERS


def exit(*args, **kwargs):
    """
        Initialization exit. Kill all processes, delete socket and stop service.
    """
    ANSWERS = kwargs['ANS']
    STARTED_PROCESSES = kwargs['SP']
    if STARTED_PROCESSES:
        for name, process in STARTED_PROCESSES.items():
                try:
                    process.terminate()
                    info('I stopped process %s' % name)
                    del STARTED_PROCESSES[name]
                    ANSWERS += 'Killed process %s\n' % name
                except:
                    # TODO what i must doing if process is not dead?
                    ANSWERS += 'Can\'t kill process %s\n' % name
                    critical('I can\'t terminate process %s' % name)
        ANSWERS += 'Killed all processes.\n'
        ANSWERS += 'Exit from service.'
    else:
        debug('All processes are dead')
        ANSWERS = 'All processes are dead.'
    STARTED_PROCESSES['exit'] = True
    return ANSWERS, STARTED_PROCESSES


def kill(*args, **kwargs):
    """
        Killer for processes. Can kill one or all.
    """
    ANSWERS = kwargs['ANS']
    STARTED_PROCESSES = kwargs['SP']
    ATTR = kwargs['ATTR']
    if ATTR:
        ANSWERS = 'hello world'
    else:
        if STARTED_PROCESSES:
            for name, process in STARTED_PROCESSES.items():
                try:
                    process.terminate()
                    info('I stopped process %s' % name)
                    del STARTED_PROCESSES[name]
                    ANSWERS += 'Killed process %s\n' % name
                except:
                    # TODO what i must doing if process is not dead?
                    ANSWERS += 'Can\'t kill process %s\n' % name
                    critical('I can\'t terminate process %s' % name)
            ANSWERS += 'Killed all processes.\n'
            ANSWERS += 'Working in background.'
        else:
            debug('All processes are dead')
            ANSWERS = 'All processes are dead.'
    return ANSWERS, STARTED_PROCESSES