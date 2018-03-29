# coding: utf-8
import time
import os

__author__ = 'Dmitry Kryukov'


def nox():
    while True:
        print 'I am a child %s in process %s' % ('nox', os.getpid())
        time.sleep(10)