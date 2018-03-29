# coding: utf-8
import time
import os

__author__ = 'Dmitry Kryukov'


def nibbler():
    while True:
        print 'I am a child %s in process %s' % ('nibbler', os.getpid())
        time.sleep(10)
