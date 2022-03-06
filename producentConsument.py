"""
Module representing second task in week 3 from course Paralel programming and distributed systems
"""

from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
from random import randint


class LightSwitch:
    """
    Light switch from first task
    """

    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.lock()
        self.counter = self.counter + 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter = self.counter - 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class Shared:
    def __init__(self, buffer_size):
        self.items = Semaphore(1)
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(buffer_size)


def producer(shared_obj):
    while True:
        sleep(randint(1, 10)/10)  # producing item (even when buffer is full)
        print("P")
        shared_obj.free.wait()
        if shared_obj.finished:
            break
        shared_obj.mutex.lock()
        sleep(randint(1, 10)/10)  # adding item
        shared_obj.mutex.unlock()
        shared_obj.items.signal()


def consumer(shared_obj):
    while True:
        shared_obj.items.wait()
        if shared_obj.finished:
            break
        shared_obj.mutex.lock()
        sleep(randint(1, 10)/10)  # taking item
        shared_obj.mutex.unlock()
        shared_obj.free.signal()
        print("C")
        sleep(randint(1, 10)/10)  # processing item


for i in range(10):
    shared = Shared(10)
    consumers = [Thread(consumer, shared) for _ in range(2)]
    producers = [Thread(producer, shared) for _ in range(5)]
    sleep(5)
    shared.finished = True
    print(f"main thread {i} waiting for the end")
    shared.items.signal(40)
    shared.free.signal(40)
    [t.join() for t in consumers+producers]
    print(f"main thread {i} ended")
