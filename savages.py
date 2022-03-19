"""
Assignment savages, week 5
Author: David Gellen
Used resources: https://www.youtube.com/watch?v=iotYZJzxKf4,
https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-%f0%9f%9a%ac/
"""

from random import randint
from fei.ppds import Mutex, Semaphore, Thread, print
from time import sleep


class Shared:
    """
    Class holding all the synchronization tools
    servings - servings remaining in the pot
    mutex - mutex for savages
    mutex2 - mutex for cooks
    empty_pot - signals empty pot
    full_pot - signals full pot
    barrier, barrier2 - barriers for savages
    """
    def __init__(self):
        self.servings = 0
        self.mutex = Mutex()
        self.mutex2 = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.barrier = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)


class SimpleBarrier:
    """
    Simple barrier class
    n: number of threads
    counter: thread counter
    mutex: mutex for counter check
    event: event for blocking/unblocking the barrier
    """
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.sem = Semaphore(0)

    """
    Implementation of wait method on barrier. Each thread waits for event signalisation, after which the program
    continues and the last thread clears the event signalisation.
    """
    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.sem.signal(self.n)
        self.mutex.unlock()
        self.sem.wait()


def savage(savage_, shared):
    """
    savage eatings servings, waiting to start together using barrier
    :param savage_: savage id
    :param shared: shared object with synchronization tools
    """
    sleep(randint(1, 100)/100)
    while True:
        shared.barrier.wait()
        shared.barrier2.wait()
        shared.mutex.lock()
        if shared.servings == 0:
            print(f"savage {savage_}: empty pot")
            shared.empty_pot.signal(M)
            shared.full_pot.wait()
        print(f"savage {savage_}: taking from pot")
        shared.servings -= 1
        shared.mutex.unlock()
        eat(savage_)


def eat(savage_):
    """
    savage eating
    :param savage_: savage id
    """
    # print(f"savage {savage_} eating")
    sleep(randint(50, 200)/100)


def cook(i, shared):
    """
    cook producing a serving
    each cook produces a full serving by himself
    :param i: cook id
    :param shared: shared object with synchronization tools
    """
    while True:
        shared.empty_pot.wait()
        shared.mutex2.lock()
        if shared.servings < M:
            print(f'cook {i}: cooking')
            sleep(randint(1, 5)/10)
            shared.servings += 1
            if shared.servings == M:
                shared.full_pot.signal()
                # shared.empty_pot.wait()
        shared.mutex2.unlock()


def run():
    """
    main method to test functionality
    """
    shared = Shared()
    savages = []
    cooks = []
    for s in range(N):
        savages.append(Thread(savage, s, shared))
    for c in range(C):
        cooks.append(Thread(cook, c, shared))

    for t in savages + cooks:
        t.join()


N = 3
M = 10
C = 4


if __name__ == "__main__":
    run()
