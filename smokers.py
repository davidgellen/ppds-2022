"""
Assignment smokers, week 5
Author: David Gellen
Used resources: https://www.youtube.com/watch?v=iotYZJzxKf4
"""

from random import randint
from fei.ppds import Mutex, Semaphore, Thread, print
from time import sleep


class Shared:
    """
    Class holding all the synchronization tools
    tobacco, paper, match - production of resources by agents
    dealer_match, dealer_match, dealer_tobacco - produced resourced given to shared space by dealers
    mutex - global mutex
    has_tobacco, has_paper, has_match - amount of resources in shared space provided by dealers
    """
    def __init__(self):
        self.agentSem = Semaphore(1)
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)
        self.dealer_match = Semaphore(0)
        self.dealer_paper = Semaphore(0)
        self.dealer_tobacco = Semaphore(0)
        self.mutex = Mutex()
        self.has_tobacco = 0
        self.has_paper = 0
        self.has_match = 0


def agent_1(shared):
    """
    agent producing tobacco and paper
    :param shared: shared object with synchronization tools
    """
    while True:
        sleep(randint(0, 10)/100)
        # shared.agentSem.wait()
        print("agent: tobacco, paper")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    """
    agent producing paper and a match
    :param shared: shared object with synchronization tools
    """
    while True:
        sleep(randint(0, 10)/100)
        # shared.agentSem.wait()
        print("agent: paper, match")
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared):
    """
    agent producing tobacco and a match
    :param shared: shared object with synchronization tools
    """
    while True:
        sleep(randint(0, 10)/100)
        # shared.agentSem.wait()
        print("agent: tobacco, match")
        shared.tobacco.signal()
        shared.match.signal()


def make_cigarette(name):
    """
    simulation of cigarette making
    :param name: smoker's infinite resource
    """
    print(f"smoker {name} making cigarette")
    sleep(randint(0, 10)/100)


def smoke(name):
    """
    simulation of smoking
    :param name: smoker's infinite resource
    """
    # print(f"smoker {name} smoking")
    sleep(randint(0, 10)/100)


def smoker_match(shared):
    """
    function representing smoker with infinite matches
    :param shared: shared object with synchronization tools
    """
    while True:
        sleep(randint(0, 10)/100)
        shared.dealer_match.wait()
        make_cigarette("match")
        shared.agentSem.signal()
        smoke("match")


def smoker_tobacco(shared):
    """
    function representing smoker with infinite tobacco
    :param shared: shared object with synchronization tools
    """
    while True:
        sleep(randint(0, 10)/100)
        shared.dealer_tobacco.wait()
        make_cigarette("tobacco")
        shared.agentSem.signal()
        smoke("tobacco")


def smoker_paper(shared):
    """
    function representing smoker with infinite paper
    :param shared: shared object with synchronization tools
    """
    while True:
        sleep(randint(0, 10)/100)
        shared.dealer_paper.wait()
        make_cigarette("paper")
        shared.agentSem.signal()
        smoke("paper")


def dealer_match_old(shared):
    """
    match dealer function original
    :param shared: shared object with synchronization tools
    """
    while True:
        shared.match.wait()
        shared.mutex.lock()

        if shared.has_tobacco > 0:
            shared.has_tobacco -= 1
            shared.dealer_paper.signal()
        elif shared.has_paper > 0:
            shared.has_paper -= 1
            shared.dealer_tobacco.signal()
        else:
            shared.has_match += 1
        print(f"RESOURCES: paper {shared.has_paper}, tobacco {shared.has_tobacco}, matches {shared.has_match}")
        shared.mutex.unlock()


def dealer_match(shared):
    """
    match dealer function new version
    :param shared: shared object with synchronization tools
    """
    while True:
        shared.match.wait()
        shared.mutex.lock()

        if shared.has_tobacco > 0 and shared.has_paper > 0:

            if shared.has_tobacco == shared.has_paper:
                decision = randint(0, 1)  # chosen randomly if same amount of resources is present
                if decision == 1:
                    shared.has_tobacco -= 1
                    shared.dealer_paper.signal()
                else:
                    shared.has_paper -= 1
                    shared.dealer_tobacco.signal()

            if shared.has_tobacco > shared.has_paper:
                shared.has_tobacco -= 1
                shared.dealer_paper.signal()
            else:
                shared.has_paper -= 1
                shared.dealer_tobacco.signal()

        else:
            shared.has_match += 1
        print(f"RESOURCES: paper {shared.has_paper}, tobacco {shared.has_tobacco}, matches {shared.has_match}")
        shared.mutex.unlock()


def dealer_paper_old(shared):
    """
    paper dealer function original
    :param shared: shared object with synchronization tools
    """
    while True:
        shared.paper.wait()

        shared.mutex.lock()
        if shared.has_tobacco > 0:
            shared.has_tobacco -= 1
            shared.dealer_match.signal()
        elif shared.has_match > 0:
            shared.has_match -= 1
            shared.dealer_tobacco.signal()
        else:
            shared.has_paper += 1
        print(f"RESOURCES: paper {shared.has_paper}, tobacco {shared.has_tobacco}, matches {shared.has_match}")

        shared.mutex.unlock()


def dealer_paper(shared):
    """
    paper dealer function new version
    :param shared: shared object with synchronization tools
    """
    while True:
        shared.paper.wait()
        shared.mutex.lock()

        if shared.has_tobacco > 0 and shared.has_match > 0:

            if shared.has_tobacco == shared.has_match:
                decision = randint(0, 1)  # chosen randomly if same amount of resources is present
                if decision == 1:
                    shared.has_tobacco -= 1
                    shared.dealer_match.signal()
                else:
                    shared.has_match -= 1
                    shared.dealer_tobacco.signal()

            if shared.has_tobacco > shared.has_match:
                shared.has_tobacco -= 1
                shared.dealer_match.signal()
            else:
                shared.has_match -= 1
                shared.dealer_tobacco.signal()

        else:
            shared.has_paper += 1
        print(f"RESOURCES: paper {shared.has_paper}, tobacco {shared.has_tobacco}, matches {shared.has_match}")
        shared.mutex.unlock()


def dealer_tobacco_old(shared):
    """
    tobacco dealer function original
    :param shared: shared object with synchronization tools
    """
    while True:
        shared.tobacco.wait()

        shared.mutex.lock()
        if shared.has_paper > 0:
            shared.has_paper -= 1
            shared.dealer_match.signal()
        elif shared.has_match > 0:
            shared.has_match -= 1
            shared.dealer_paper.signal()
        else:
            shared.has_tobacco += 1
        print(f"RESOURCES: paper {shared.has_paper}, tobacco {shared.has_tobacco}, matches {shared.has_match}")

        shared.mutex.unlock()


def dealer_tobacco(shared):
    """
    tobacco dealer function new version
    :param shared: shared object with synchronization tools
    """
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()

        if shared.has_paper > 0 and shared.has_match > 0:

            if shared.has_paper == shared.has_match:
                decision = randint(0, 1)  # chosen randomly if same amount of resources is present
                if decision == 1:
                    shared.has_paper -= 1
                    shared.dealer_match.signal()
                else:
                    shared.has_match -= 1
                    shared.dealer_paper.signal()

            if shared.has_paper > shared.has_match:
                shared.has_paper -= 1
                shared.dealer_match.signal()
            else:
                shared.has_match -= 1
                shared.dealer_paper.signal()

        else:
            shared.has_tobacco += 1
        print(f"RESOURCES: paper {shared.has_paper}, tobacco {shared.has_tobacco}, matches {shared.has_match}")
        shared.mutex.unlock()


def run():
    """
    main method to test functionality
    """
    shared = Shared()
    agents = [Thread(agent_1, shared), Thread(agent_2, shared), Thread(agent_3, shared)]
    dealers = [Thread(dealer_match_old, shared), Thread(dealer_paper_old, shared), Thread(dealer_tobacco_old, shared)]
    smokers = [Thread(smoker_match, shared), Thread(smoker_tobacco, shared), Thread(smoker_paper, shared)]

    for t in smokers + agents + dealers:
        t.join()


if __name__ == "__main__":
    run()
