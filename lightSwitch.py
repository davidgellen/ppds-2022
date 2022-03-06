"""
Module representing first task in week 3 from course Paralel programming and distributed systems
"""

from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
from random import randint


class LightSwitch:
    """
    Abstract representation of light switch synchronization model
    counter: number of objects entering a state
    mutex: mutex for checking the counter
    """
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.lock()
        self.counter = self.counter + 1
        if self.counter == 1:
            print("1st switching on")
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter = self.counter - 1
        if self.counter == 0:
            print("last switching off")
            semaphore.signal()
        self.mutex.unlock()


def example_function(light_switch, i, semaphore):
    """
    Test function, each thread enters light switch, first one locking the semaphore and last one unlocking it
    after exiting the critical area
    :param light_switch: light switch object
    :param i: thread id
    :param semaphore: semaphore to handle via light switch
    :return: nothing
    """
    light_switch.lock(semaphore)
    print(str(i) + " in KO")
    sleep(randint(1, 10)/10)
    print(str(i) + " ending KO")
    light_switch.unlock(semaphore)


THREADS = 5
sem = Semaphore(1)
ls = LightSwitch()
threads = [Thread(example_function, ls, i, sem) for i in range(THREADS)]
[t.join() for t in threads]
sem.wait()
print("code still executes, no new line will be printed due to triggered deadlock via semaphore.wait()")
sem.wait()
print("deadlock, this will not be printed")
