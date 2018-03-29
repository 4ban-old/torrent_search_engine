# coding: utf-8
import time
import os

__author__ = 'Dmitry Kryukov'


def pudge():
    while True:
        print 'I am a child %s in process %s' % ('pudge', os.getpid())
        time.sleep(10)
