# Week 6

The implementation is a modification of pseudocode from lecture https://www.youtube.com/watch?v=IOeO6RDhhac&t=2079s.

## Task

Implement a barbershop. Customers keep coming to the waiting room of the barbershop and are put in a queue. 
Barber always calls in the customer at the front of the queue to get a haircut. 
The barbershop has a capacity and if there are no more places in available in the waiting room, no one can come in.

### Synchronization tools:
```
class Shared:
    def __init__(self, n, total_customers):
        self.mutex = Mutex()
        self.n = n
        self.total_customers = total_customers
        self.customers = 0
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)
        self.queue = []
        self.customer = Semaphore(0)
        self.barbers = [Semaphore(0) for _ in range(total_customers)]
```
mutex - for integrity check


__n__ - number of total seats in barbershop (includes seat where barber cuts hair - total places in waiting
    room are n - 1)


__total_customers__ - total number of customers

__customers__ - current customers count

__customer_done__ - signals once customer is finished getting a haircut

__barber_done__ - signals once barber is finished giving a haircut

__barbers__ - list of semaphores for each customer of the barbershop, synchronizing with customer

__customer__ - synchronizing with each semaphore in barbers, barber stars cutting hair after mutual synchronization


### Customer's routine:
```
def customer(id_, shared):
    sleep(randint(1, 20)/10)
    while True:
        sleep(randint(10, 14)/10)
        shared.mutex.lock()
        if shared.customers == shared.n:
            print(f"waiting room full, {id_} has to come back later")
            shared.mutex.unlock()
            continue
        shared.customers += 1
        shared.queue.append(shared.barbers[id_])
        print(f"customer {id_} sitting down in waiting room")
        shared.mutex.unlock()

        shared.customer.signal()
        shared.barbers[id_].wait()

        get_haircut(id_)

        shared.customer_done.signal()
        shared.barber_done.wait()

        shared.mutex.lock()
        shared.customers -= 1

        shared.mutex.unlock()
```
### Barber's routine:
```
def barber(shared):
    while True:
        shared.customer.wait()
        shared.mutex.lock()
        next_in_line = shared.queue.pop(0)
        next_in_line.signal()
        shared.mutex.unlock()

        cut_hair()

        shared.customer_done.wait()
        shared.barber_done.signal()
```

Once the threads are initialized, barber is ready to be woken up but no one is in the waiting room yet. Once the customers start coming in, 
they go to the waiting room and current count increments and customer is put in a queue - that is if there are spaces available to sit on in the waiting room. If the waiting room is full, customer doesn't come in a returns later.
Customer also signalizes that he's in waiting room so barber knows that he can call him up to get a haircut.

Once customer is called up, he/she gets a haircut, barber signalizes that he's done giving a haircut and customers signalizes that he/she's done getting one.
After that, one the seat that the customer occupied becomes available for new customers.

__File:__ barbershop.py