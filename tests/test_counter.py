import timeit
import random
import string
from collections import Counter

letters = string.letters
l = []
for x in range(10000):
    a = random.choice(letters)
    l.append(a)

class MyCounter(dict):
    def __setattr__(self, key, value):

        if key not in self:
            super(MyCounter, self).__setitem__(key, value)
        self.__setattr__(key, value+self[key])


def with_d(lst):
    d = dict()
    l = len(lst)
    for n, a in enumerate(lst):
        w = l - n
        d[a] = d[a] + w if a in d else w
    return d

def with_c(lst):
    c = Counter()
    l = len(lst)
    for n, a in enumerate(lst):
        w = l - n
        c[a] += w
    return c

def with_mc(lst):
    c = MyCounter()
    l = len(lst)
    for n, a in enumerate(lst):
        w = l - n
        c[a] = w

    return c

t1 = timeit.timeit('with_d(l)', setup='from __main__ import with_d, l', number=1000)
t2 = timeit.timeit('with_c(l)', setup='from __main__ import with_c, l', number=1000)
t3 = timeit.timeit('with_mc(l)', setup='from __main__ import with_mc, l', number=1000)
print t1, t2, t3
print float(t1)/t2, float(t2)/t3, float(t1)/t3
