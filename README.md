# Week 1

Assignment focuses on basics of parallel programming using module fei.ppds and matplotlib for visual interpretation via histograms. This implementation is a modification of source code presented on lecture Paralel programming and distributed systems from 16/02/2022.

## Task:

Implement 2 threads which use the same index pointing to shared array of given size. Each thread increments element of the array pointed at by the index and increases the index itself. Once the index points out of bounds of the array, thread stops it' s execution.


Class Shared - holds array (elms), index (counter) pointing at element of the array and size (end) of the array initialized with zeroes.
```
class Shared:
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size
```


Function used to increment element values and index (non-parallel implementation, is not part of the actual code).
```
    def do_count(shared_obj):
    while shared_obj.counter < shared_obj.end:
        shared_obj.elms[shared_obj.counter] += 1
        shared_obj.counter += 1
```
To get a general idea, desired outcome would be that all elements in the array have value of 1 and index == size of the array.
However, running this code results in state where not all elements are equal to 1. We can observe that a decent amount of elements have
a value of 2 - both threads increment the element pointed at by the index before the index itself gets incremented.

Note: we read as follows (value: amount of elements in an array with value)
```
[(1, 889118), (2, 110881), (0, 1)]
```


### 1st alternative:

If index does not point outside the array, current thread locks the lock, therefore other thread is unable to change
neither the array nor the index. Once the thread that locked the lock increments index value and the corresponding 
element in the array, lock is unlocked and other thread is able to start the same routine without receiving corrupted
data nor corrupting the data for other thread.

Note: this implementation results in the last expected iteration trying to access element out of bounds, hence we add
condition to check the index after locking
```
    def do_count(shared_obj, mutex_obj):
    while shared_obj.counter < shared_obj.end:
        mutex_obj.lock()
        # last expected iteration tries to access element out of bounds resulting in exception, therefore we check
        # the condition also after the lock
        if shared_obj.counter < shared_obj.end:
            shared_obj.elms[shared_obj.counter] += 1
            shared_obj.counter += 1
        mutex_obj.unlock()
```

File: week1_1.py

#### Results
Size = 1000, no exception
```
[(1, 1000)]
```
Size = 1000000, no exception
```
[(1, 1000000)]
```
Size = 100000000, no exception
```
[(1, 100000000)]
```

### 2nd alternative:

We lock the lock before iterating through the array and unlock it only after every element and the index have been incremented to expected values.
This way we achieve that the thread responsible for locking the lock iterates through the array alone. This kind of implementation is useful f.e. if we 
want to have the function run independently on multiple threads.

```
def do_count(shared_obj, mutex_obj):
    mutex_obj.lock()
    while shared_obj.counter < shared_obj.end:
        shared_obj.elms[shared_obj.counter] += 1
        shared_obj.counter += 1
    mutex_obj.unlock()
```

File: week1_2.py

#### Results
Size = 1000, no exception
```
[(1, 1000)]
```
Size = 1000000, no exception
```
[(1, 1000000)]
```
Size = 100000000, no exception
```
[(1, 100000000)]
```

Results are same as in the 1st alternative. This way, however, is much faster due to locking/unlocking only once in comparison with locking/unlocking size of the array times as in the 1st alternative.