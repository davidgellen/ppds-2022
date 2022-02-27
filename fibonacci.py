from time import sleep
from random import randint
from fei.ppds import Thread, Event, Semaphore, print


class Adt:
    """
    Class holding list of Semaphores of size n + 1, each corresponding to thread with same id as index of the Semaphore
    """
    def __init__(self, n):
        self.n = n
        self.sync_tool = [Event() for _ in range(n)]  # shallow copy of Event(), deep copy would signal everything
        # self.sync_tool = [Semaphore(0) for i in range(n)]  # works with Semaphore too
        self.sync_tool[0].signal()  # signals for first number

    """
    Method waits for semaphore signalisation and signals for next thread's semaphore 
    (first one signaling in constructor)
    :i : id/index of current thread
    """
    def wait(self, i):
        self.sync_tool[i].wait()
        try:  # for last Thread in list
            self.sync_tool[i + 1].signal()
        except:
            print("finished")


def compute_fibonacci(adt_obj, i):
    """
    Computes the value for fibonacci sequence for index i + 2
    :param adt_obj: synchronization object
    :param i: index
    :return:
    """
    sleep(randint(1, 10) / 10)  # for visual purposes
    adt_obj.wait(i)
    fib_seq[i + 2] = fib_seq[i] + fib_seq[i + 1]


THREADS = 10
fib_seq = [0] * (THREADS + 2)
fib_seq[1] = 1
adt = Adt(10)

threads = [Thread(compute_fibonacci, adt, i) for i in range(THREADS)]
[t.join() for t in threads]

print(fib_seq)
