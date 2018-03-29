# coding: utf-8
"""
    Service for communist control.
    Listen unix_socket, communicate with human.
    Also can create child processes and communicate with them.
"""
__author__ = 'Dmitry Kryukov'

import os
from socket import *
from select import *
from logging import *
# from importlib import import_module
# from multiprocessing import Process, Pipe
import commands

# Logging settings
basicConfig(format='[%(levelname)-8s][%(asctime)s][%(filename)s][%(funcName)s] in process %(process)d %(processName)s - %(message)s',
            level=DEBUG,
            filename='./service.log',
            datefmt='%H:%M:%S %d/%m/%Y')
# Settings
UNIX_SOCKET = './service_socket'
COUNT_CONNECTION = 5
TIMEOUT = 3
STARTED_PROCESSES = dict()
# TODO fucking crutch =(
ANSWERS = ''


def service():
    """
        Function listen UNIX socket for connection and wait message for some action.
        Parallel with waiting function controlling child processes.
    """
    # TODO find exception
    sock = socket(AF_UNIX, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # TODO find exception
    sock.bind(UNIX_SOCKET)
    sock.listen(COUNT_CONNECTION)
    info('Service starting listening socket.')
    connection_list = [sock]
    message = ''
    global ANSWERS
    try:
        while True:
            try:
                if STARTED_PROCESSES['exit']:
                    raise KeyboardInterrupt
            except KeyError:
                pass

            to_input, to_output, exc = select(connection_list, [], [], TIMEOUT)
            if to_input:
                for s in to_input:
                    if s is sock:
                        connection, address = s.accept()
                        info('Service detected connection.')
                        connection_list.append(connection)
                    else:
                        try:
                            message = connection.recv(1024)
                            info('Service received message: %s' % message)
                            if message:
                                commander(message)
                                message = ''  # delete message after call by commander
                            if ANSWERS:
                                connection.send(ANSWERS)
                                ANSWERS = ''
                            else:
                                pass
                                #connection.send('Have no answer for you.')
                            info('Service send answer back.')
                        except:
                            warning('I found error when tried to get message.')
                        finally:
                            connection.close()
                            connection_list.remove(connection)
                            info('Service close connection.')
    except KeyboardInterrupt:
        warning('Detect keyboard interrupt. Stopping service. Close socket.')
        # TODO Make stop initialization
        if STARTED_PROCESSES:
            for name, process in STARTED_PROCESSES.items():
                try:
                    process.terminate()
                    info('I stopped process %s' % name)
                    del STARTED_PROCESSES[name]
                except:
                    # TODO what i must doing if process is not dead?
                    critical('I can\'t terminate process %s' % name)
        else:
            debug('All processes are dead')
        sock.close()
        os.remove(UNIX_SOCKET)
    finally:
        # TODO Make stop initialization
        if STARTED_PROCESSES:
            for name, process in STARTED_PROCESSES.items():
                try:
                    process.terminate()
                    info('I stopped process %s' % name)
                    del STARTED_PROCESSES[name]
                except:
                    # TODO what i must doing if process is not dead?
                    critical('I can\'t terminate process %s' % name)
        else:
            debug('All processes are dead')
        sock.close()
        if os.path.exists(UNIX_SOCKET):
            os.remove(UNIX_SOCKET)


def commander(message):
    """
        Function parse message on commands and try to do them.
    :param message: like "start pudge [attr]"
    """
    # TODO add defaults commands to config
    defaultCmdList = ['status', 'kill', 'exit', 'help', 'run', ]
    global ANSWERS
    if message:
        message = message.strip(' ').lower()
        message = message.split(' ', 1)
        if message[0] in defaultCmdList:
            action = getattr(commands, message[0], None)
            attr = ''
            if len(message) > 1:
                attr = message[1]
            if message[0] == 'status' or message[0] == 'help':
                ANSWERS = action(ANS=ANSWERS, SP=STARTED_PROCESSES, ATTR=attr)
            elif message[0] == 'run' or message[0] == 'kill' or message[0] == 'exit':
                _ANSWERS, _STARTED_PROCESSES = action(ANS=ANSWERS, SP=STARTED_PROCESSES, ATTR=attr)
                ANSWERS = _ANSWERS
                STARTED_PROCESSES.update(_STARTED_PROCESSES)
            # print '================='
            # print ANSWERS
            # print '================='
        else:
            ANSWERS = 'No such command. Try again or look help.'


if __name__ == '__main__':
    info('I am running.')
    if os.path.exists(UNIX_SOCKET):
        warning('I found open UNIX socket %s. Try to close.', UNIX_SOCKET)
        os.remove(UNIX_SOCKET)
    # Initialization, first start default processes from config
    STARTED_PROCESSES.update(commands.run(firstStart=True))
    info('Starting service.')
    service()