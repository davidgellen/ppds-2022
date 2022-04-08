"""
Examples from lecture https://www.youtube.com/watch?v=vFLQgRXrA0Q by Mgr. Ing. Matúš Jókay, PhD.
Author: David Gellen
License: GPL-3.0

This is not the actual assignment
"""


class MyIterator(object):
    def __init__(self, xs):
        self.xs = xs

    def __iter__(self):
        return self

    def __next__(self):
        if self.xs:
            return self.xs.pop(0)
        else:
            raise StopIteration


def try_simple_iteration():
    for i in MyIterator([0, 1, 2]):
        print(i)


def my_generator(n):
    while n:
        n -= 1
        yield n


def try_generator1(n):
    for i in my_generator(n):
        print(i)


def try_generator2(n):
    g = my_generator(n)
    for i in range(n + 3):
        next(g)


try_generator1(5)
print()
try_generator2(2)

