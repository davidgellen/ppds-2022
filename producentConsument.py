"""
Module representing second task in week 3 from course Paralel programming and distributed systems
"""

import time
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
        self.total_added = 0
        self.total_taken = 0


def producer(shared_obj, production_time_):
    """
    Function representing producer thread
    """
    while True:
        sleep(randint(1, 10) / production_time_)  # producing item (even when buffer is full)
        # print("P")
        shared_obj.free.wait()
        if shared_obj.finished:
            break
        shared_obj.mutex.lock()
        sleep(randint(1, 10) / production_time_)  # adding item
        shared_obj.total_added = shared_obj.total_added + 1
        shared_obj.mutex.unlock()
        shared_obj.items.signal()


def consumer(shared_obj, consumption_time_):
    """
    Function representing consumer thread
    """
    while True:
        shared_obj.items.wait()
        if shared_obj.finished:
            break
        shared_obj.mutex.lock()
        sleep(randint(1, 10) / consumption_time_)  # taking item
        shared_obj.total_taken = shared_obj.total_taken + 1
        shared_obj.mutex.unlock()
        shared_obj.free.signal()
        # print("C")
        sleep(randint(1, 10) / consumption_time_)  # processing item


production_times = [10, 100]
consumption_times = [10, 100]
producers_count = [5, 50, 500]
consumers_count = [5, 50, 500]
storages = [100, 1000, 1000]

print("production_time", "consumption_time", "producer_count", "consumer_count", "storage", "time", "avg_added",
      "avg_produced")
for production_time in production_times:
    for consumption_time in consumption_times:
        for producer_count in producers_count:
            for consumer_count in consumers_count:
                for storage in storages:
                    total_added_in_iteration = 0
                    total_taken_in_iteration = 0
                    total_time_in_duration = 0
                    for i in range(10):
                        start_time = time.time()
                        shared = Shared(storage)
                        consumers = [Thread(consumer, shared, consumption_time) for _ in range(consumer_count)]
                        producers = [Thread(producer, shared, production_time) for _ in range(producer_count)]
                        sleep(5)
                        shared.finished = True
                        # print(f"main thread waiting for the end")
                        shared.items.signal(storage * 10)
                        shared.free.signal(storage * 10)
                        [t.join() for t in consumers + producers]
                        # print(f"main thread ended")
                        end_time = time.time()
                        time_difference = end_time - start_time
                        total_time_in_duration = total_time_in_duration + time_difference
                        total_added_in_iteration = total_added_in_iteration + shared.total_added
                        total_taken_in_iteration = total_taken_in_iteration + shared.total_taken
                        # print("iteration done")
                    avg_total_added = total_added_in_iteration / 10
                    avg_total_taken = total_taken_in_iteration / 10
                    avg_total_time = total_time_in_duration / 10
                    print(production_time, consumption_time, producer_count, consumer_count, storage, avg_total_time,
                          avg_total_added, avg_total_taken)
                    # print("avg added:", avg_total_added)
                    # print("avg taken:", avg_total_taken)
