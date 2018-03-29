# coding: utf-8
"""
    Test client for service
"""
from socket import *
from logging import *

__author__ = 'Dmitry Kryukov'

# Logging settings
basicConfig(format='[%(levelname)-8s][%(asctime)s][%(filename)s][%(funcName)s] in process %(process)d %(processName)s - %(message)s',
            level=DEBUG,
            filename='./service.log',
            datefmt='%H:%M:%S %d/%m/%Y')

server_address = './service_socket'
print """Controller for service.
Commands:
    status [name ...]  -> print status all processes or selected process
    kill name ...      -> kill process
    run name           -> start process
    exit               -> exit for service
    help [command ...] -> help for service or each command
    =================================================================
"""
debug('Started client')
try:
    while True:
        try:
            s = socket(AF_UNIX, SOCK_STREAM)
            s.connect(server_address)
            message = raw_input('\033[32m>>>\033[0m ')
            print '\033[32mSending "\033[34m%s\033[32m"\033[0m' % message
            s.sendall(message)
            debug('Client send message: %s', message)
            data = s.recv(1024)
            print '\033[34m<<<\033[0m\n%s' % data
            debug('Client get answer.')
            s.close()
        except error, msg:
            print '==========================================================='
            print 'Can\'t connect to socket. Is service running?'
            debug('Client can\'t connect to sosket.')
            print error, msg
            print '==========================================================='
            raise KeyboardInterrupt
except KeyboardInterrupt:
    print '\nDetect exit. Stop client. Closing socket.'
    debug('Client exit.')
    s.close()