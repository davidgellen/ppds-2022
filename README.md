# Week 3

Assignment focuses on producer/consumer and writer/reader concepts.
This implementation is a modification of source code presented on lecture Paralel programming and distributed systems webpage of the course https://uim.fei.stuba.sk/i-ppds/3-cvicenie-fibonacci-vypinac-p-k-c-z-%f0%9f%92%a1/?%2F).

## Task 1:

Implement ADT Lightswitch.


Class SimpleBarrier - holds number of threads (n), counter of threads waiting (counter), mutex and event objects.
```
class LightSwitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0
```


Implementation of lock functionality.
```
    def lock(self, semaphore):
        self.mutex.lock()
        self.counter = self.counter + 1
        if self.counter == 1:
            print("1st switching on")
            semaphore.wait()
        self.mutex.unlock()
```

Implementation of unlock functionality.def unlock(self, semaphore):
```
    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter = self.counter - 1
        if self.counter == 0:
            print("last switching off")
            semaphore.signal()
        self.mutex.unlock()
```

Example of usage can be seen in method example_function.

File: lightSwitch.py

## Task 2:

Implement a producer/consumer method using ADT Lightswitch from Task 1.

Producer:
```
def producer(shared_obj, production_time_):
    while True:
        sleep(randint(1, 10) / production_time_)  # producing item (even when buffer is full)
        shared_obj.free.wait()
        if shared_obj.finished:
            break
        shared_obj.mutex.lock()
        sleep(randint(1, 10) / production_time_)  # adding item
        shared_obj.total_added = shared_obj.total_added + 1
        shared_obj.mutex.unlock()
        shared_obj.items.signal()
```

Consumer:
```
def consumer(shared_obj, consumption_time_):
    while True:
        shared_obj.items.wait()
        if shared_obj.finished:
            break
        shared_obj.mutex.lock()
        sleep(randint(1, 10) / consumption_time_)  # taking item
        shared_obj.total_taken = shared_obj.total_taken + 1
        shared_obj.mutex.unlock()
        shared_obj.free.signal()
        sleep(randint(1, 10) / consumption_time_)  # processing item
```
Experimental values for parameters:
```
production_times = [10, 100]
consumption_times = [10, 100]
producers_count = [5, 50, 500]
consumers_count = [5, 50, 500]
storages = [100, 1000, 1000]
```
Program iterates through these values and keeps track of produced items, consumed items and time of these activities.
Each parameter set takes place 10 times and the results are averaged and printed to the console.

File: producerConsumer.py
