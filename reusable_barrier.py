from time import sleep
from random import randint
from fei.ppds import Thread, Event, Mutex, print


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
        self.event = Event()

    """
       Implementation of wait method on barrier. Each thread waits for event signalisation, after which the program
       continues and the last thread clears the event signalisation.
       """
    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()
        # clearing with last thread after event.wait()
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            self.event.clear()
        self.mutex.unlock()


def rendezvous(thread_name):
    sleep(randint(1, 10)/10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10)/10)


def barrier_example(barrier_1, barrier_2, thread_id):
    while True:
        rendezvous(thread_id)
        barrier_1.wait()
        ko(thread_id)
        barrier_2.wait()


THREADS = 5
sb_1 = SimpleBarrier(THREADS)
sb_2 = SimpleBarrier(THREADS)
threads = list()
for i in range(5):
    t = Thread(barrier_example, sb_1, sb_2, 'Thread %d' % i)
    threads.append(t)

for t in threads:
    t.join()
