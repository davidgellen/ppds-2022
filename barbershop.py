"""
PPDS week 6 - barbershop
Author: Bc. David Gellen
Resources: Lecture https://www.youtube.com/watch?v=IOeO6RDhhac&t=2078s by Mgr. Ing. Matúš Jókay, PhD.
"""
from random import randint
from fei.ppds import Mutex, Semaphore, Thread, print
from time import sleep


class Shared:
    """
    synchronization tools
    mutex - for integrity check
    n - number of total seats in barbershop (includes seat where barber cuts hair - total places in waiting
        room are n - 1)
    total_customers - total number of customers
    customers - current customers count
    customer_done - signals once customer is finished getting a haircut
    barber_done - signals once barber is finished giving a haircut
    barbers - list of semaphores for each customer of the barbershop, synchronizing with customer
    customer - synchronizing with each semaphore in barbers, barber stars cutting hair after mutual synchronization
    """
    def __init__(self, n, total_customers):
        """
        constructor
        :param n: number of total seats in barbershop (includes seat where barber cuts hair - total places in waiting
                  room are n - 1)
        :param total_customers: total number of customers
        """
        self.mutex = Mutex()
        self.n = n
        self.total_customers = total_customers
        self.customers = 0
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)
        self.queue = []
        self.customer = Semaphore(0)
        self.barbers = [Semaphore(0) for _ in range(total_customers)]


def customer(id_, shared):
    """
    customer comes to waiting room, sits if there's place available and if not, comes back later
    if he sits, he/she 's put into a queue and called by barber once it's his/her time to get a haircut
    once customer gets a haircut, he leaves the barbeshop and his place another one can come to the waiting room
    :param id_: customer's id
    :param shared: object with sycnhronization tools
    """
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
        # print(f"{id_} customer leaving barbershop")
        shared.mutex.unlock()


def get_haircut(id_):
    """
    simulates getting haircut
    :param id_: id of customer (for printing purposes)
    """
    print(f"{id_} getting haircut")
    sleep(randint(1, 2)/10)


def barber(shared):
    """
    barber's routine - waiting for the next customer in queue to sit and cuts his/her hair
    and letting next customer in line know to come
    :param shared: object with sychronization tools
    """
    while True:
        shared.customer.wait()
        shared.mutex.lock()
        next_in_line = shared.queue.pop(0)
        next_in_line.signal()
        shared.mutex.unlock()

        cut_hair()

        shared.customer_done.wait()
        shared.barber_done.signal()

        # print(f"barber ready for new customer")
        print()


def cut_hair():
    """
    simulates cutting hair by barber
    """
    # print("barber giving haircut")
    sleep(randint(1, 2)/10)


def run():
    """
    main method to test functionality
    """
    n = 10
    total_customers = 20
    shared = Shared(n, total_customers)
    customers = []
    for s in range(total_customers):
        customers.append(Thread(customer, s, shared))
    barber_ = Thread(barber, shared)
    for t in customers + [barber_]:
        t.join()


if __name__ == "__main__":
    run()
