from fei.ppds import Thread, Mutex, Event, print


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


def barrier_example(barrier, thread_id):
    print("thread %d before barrier" % thread_id)
    barrier.wait()
    print("thread %d after barrier" % thread_id)


THREADS = 10
sb = SimpleBarrier(THREADS)
threads = [Thread(barrier_example, sb, i) for i in range(THREADS)]
[t.join() for t in threads]
