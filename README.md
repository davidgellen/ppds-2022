# Week 2

Assignment focuses on understanding the concept of barrier using module fei.ppds.
This implementation is a modification of source code presented on lecture Paralel programming and distributed systems from 23/02/2022 and webpage of the course (https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F).

## Task 1:

Implement ADT Simple Barrier using Event mechanism.


Class SimpleBarrier - holds number of threads (n), counter of threads waiting (counter), mutex and event objects.
```
class SimpleBarrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()
```


Implementation of barrier's wait functionality.
```
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
```

First 6 lines are a basic barrier, counter increments in each of the Threads and once all the Threads run through that code,
event signals and therefore all the Threads can continue their routine. Last Thread that triggered the signalling does not wait since the signal
takes place before the waiting.

After that, we again wait for the last thread to go through the wait() and only then we call clear() on the event.

Since both parts of the function check the counter, mutex needs to be locked and unlocked respectively.

File: simple_barrier.py

#### Results
5 threads:
```
thread 4 before barrier
thread 0 before barrier
thread 2 before barrier
thread 3 before barrier
thread 1 before barrier
thread 1 after barrier
thread 4 after barrier
thread 2 after barrier
thread 3 after barrier
thread 0 after barrier
```
10 threads:
```
thread 9 before barrier
thread 7 before barrier
thread 2 before barrier
thread 3 before barrier
thread 1 before barrier
thread 6 before barrier
thread 5 before barrier
thread 4 before barrier
thread 8 before barrier
thread 0 before barrier
thread 0 after barrier
thread 1 after barrier
thread 9 after barrier
thread 3 after barrier
thread 8 after barrier
thread 5 after barrier
thread 2 after barrier
thread 7 after barrier
thread 6 after barrier
thread 4 after barrier
```
The function used for testing calls sleep, without it the thread ids would before barrier would
be in ascending order and after the barrier in descending order - threads would automatically execute code in order of their creation.

## Task 2:

Implement a reusable barrier with Event (same principle as Task 1).

Our implementation from Task 1 works directly with Task 2, so class SimpleBarrier is unchanged. The implementation was tested on function provided on the webpage.

File: reusable_barrier.py

#### Results
Same as in Task 1 but the before/after barrier console prints keep repeating themselves (due to unbreakable While True:) with shaken up ids (due to sleep).

We will not provide the console print this time since the infinite loop prints a lot of lines and it would take up a lot of space.
## Task 3:

Create N threads. Let i represent a node in which the element at position i + 2 of the Fibonacci sequence (0, 1, 1, 2, 3, 5, 8, 13, 21…) is calculated.
Let all threads share a common list in which the calculated sequence elements are stored sequentially during the calculation.
Let the first two elements 0 and 1 be fixed in this list. Using any synchronization tools, design a synchronization so that thread i can calculate 
the Fibonacci number only after all the prior threads have already calculated their numbers.

Design the synchronization in a way that uses either Semaphore or Event interchangeably without any need to change the logic of the code itself.

All threads need to be created before the calculation of the sequence itself begins.

Class Adt representing the synchronization object with number of threads (n) and own synchronization tool - array of Semaphores/Event, while only the first one calls signal().
```
class Adt:
    def __init__(self, n):
        self.n = n
        self.sync_tool = [Event() for _ in range(n)]  # shallow copy of Event(), deep copy would signal everything
        # self.sync_tool = [Semaphore(0) for i in range(n)]  # works with Semaphore too
        self.sync_tool[0].signal()  # signals for first number
```

The calculation of the fibonacci sequence is as follows:
```
def compute_fibonacci(adt_obj, i):
    sleep(randint(1, 10) / 10)  # for visual purposes
    adt_obj.wait(i)
    fib_seq[i + 2] = fib_seq[i] + fib_seq[i + 1]
```
Once again, we use sleep to "shake up" the threads.

The synchronization method of Adt called wait is simple
```
def wait(self, i):
        self.sync_tool[i].wait()
        try: # for last Thread in list
            self.sync_tool[i + 1].signal()
        except:
            print("finished")
```
Try is for raised exception due to last Thread signaling a non-existing synchronization object.

Current thread waits for signal. Once the signal is received, thread signals the next Thread and the computation can take place. 
We don't worry about deadlocks since the first element of self.sync_tool calls signal() in constructor.

#### Results
20 threads (22 elements total):
```
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946]
```
10 threads (12 elements total):
```
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```
File: fibonacci.py

### Questions:
#### What is the smallest amount of synchronization objects required to solve the problem?
We used number of threads amount of synchronization objects (N). We tried to implement a solution using 1 mutex and 1 Semaphore/Event,
but all attempted variations resulted in deadlocks. We believe it should be possible to implement a solution using 2 objects (in a "not so elegant" solution),
but since we were unable to implement such method, our final answer can only be N.

Alternatively, already signalled synchronization objects could be reused later for other Threads, but again we did not implement such functionality.

#### Which of the presented synchronization methods are applicable to this issue?
We used Semaphore/Event, so a signalization method. Thread corresponding to an element in list (fibonacci sequence) waits for signal from
Thread corresponding to prior number in the sequence, calculates the value and signals the Thread corresponding to the next number in the sequence. No mutex needed.

We personally don't see a proper usage for barrier in this task, since we never actually want to signal all the Threads to continue their routine, 
unless we would add additional conditioning + looping which seems unnecessarily complicated.

Mutex could be used if we would try implementing without a list of synchronization objects, since we would need to check values that could be overridden by other threads.
