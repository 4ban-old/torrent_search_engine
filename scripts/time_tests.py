# coding: utf-8
import timeit
import collections
import random

lst = [random.choice('qwertyuiopasdfghjklzxcvbnm019283465') for x in range(10000)]
def time_test_dict(lst):
    d = dict()
    l = len(lst)
    for n, i in enumerate(lst):
        w = l-n
        d[i] = d[i] + w if i in d else w
    return d

def time_test_counter(lst):
    d = collections.Counter()
    l = len(lst)
    for n, i in enumerate(lst):
        w = l-n
        d[i] += w
    return d

time_counter = timeit.timeit("time_test_counter(lst)", setup="from __main__ import time_test_counter, lst", number=1000)
time_dict = timeit.timeit("time_test_dict(lst)", setup="from __main__ import time_test_dict , lst", number=1000)
print 'time dict = %s \ntime counter = %s \n %s' % (time_dict, time_counter, float(time_counter/time_dict))
