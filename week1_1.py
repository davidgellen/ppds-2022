from fei.ppds import Thread, Mutex
from collections import Counter
import matplotlib.pyplot as plt


class Shared:
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size


def do_count(shared_obj, mutex_obj):
    """
    locking and unlocking the mutex in each iteration of Shared
    :param shared_obj: object of class Shared
    :param mutex_obj: initialized mutex lock
    :return:
    """
    while shared_obj.counter < shared_obj.end:
        mutex_obj.lock()
        # last expected iteration tries to access element out of bounds resulting in exception, therefore we check
        # the condition also after the lock
        if shared_obj.counter < shared_obj.end:
            shared_obj.elms[shared_obj.counter] += 1
            shared_obj.counter += 1
        mutex_obj.unlock()


mutex = Mutex()
shared = Shared(1_000_000)
t1 = Thread(do_count, shared, mutex)
t2 = Thread(do_count, shared, mutex)
t1.join()
t2.join()

counter = Counter(shared.elms)
print(counter.most_common())

plt.hist(shared.elms, bins=len(counter), align='mid')
plt.xticks(range(len(counter)))
plt.show()
