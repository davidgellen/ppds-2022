# Week 4

The implementation is a modification of source code from lecture's webpage https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-%f0%9f%9a%ac/ and lecture https://www.youtube.com/watch?v=iotYZJzxKf4

## Task1: Smokers

There are 3 smokers, 3 ingredients to make a cigarette - tobacco, match or paper, and agent providing these ingredients. Every smoker has an infinite amount of 1 resource. As agent provides resources, if smoker is able to make a cigarette, he takes the 2 resources he doesn't have an infinite supply and makes one.

Due to the synchronization issues, 3 dealers were added, to properly distribute the resources. In language of parallel programming, to prevent deadlocks.

The base functionality was explained on the lecture. The source code was as follows.

Note: we will show only source code for match dealer, tobacco and paper dealers work analogically

```
def dealer_match_old(shared):
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
```

The issue with this implementation is that match dealer always check tobacco before paper, which can create uneven distribution of resources.

Our implementation got rid of this issue.

```
def dealer_match(shared):
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

            elif shared.has_tobacco > shared.has_paper:
                shared.has_tobacco -= 1
                shared.dealer_paper.signal()
            else:
                shared.has_paper -= 1
                shared.dealer_tobacco.signal()
        elif shared.has_tobacco > 0 and shared.has_paper == 0:
            shared.has_tobacco -= 1
            shared.dealer_paper.signal()
        elif shared.has_tobacco == 0 and shared.has_paper > 0:
            shared.has_paper -= 1
            shared.dealer_tobacco.signal()
        elif shared.has_tobacco == 0 and shared.has_paper == 0:
            shared.has_match += 1
        print(f"RESOURCES: paper {shared.has_paper}, tobacco {shared.has_tobacco}, matches {shared.has_match}")
        shared.mutex.unlock()
```
If there are both paper and tobacco present, we make decision based on which resources stash is bigger (whether we have more paper or tobacco) and choose the one with bigger amount. If same amount of tobacco and paper is present, we randomly choose one. This keeps the distribution even.

If only paper or tobacco is present, we don't have to choose since we can only deal to one smoker.

If paper nor tobacco are present, we stash the match.

File: smokers.py

## Task 2: Savages

Savages take servings from shared pot. They always start together. If the pot is empty, they wake up cooks to cook up certain amount of servings. Once cooks are done cooking,
they go back to sleep.

The base with one cook was implemented on the lecture.

We are adding more cooks to work simultaneously.

### Pseudocode:

```
def run():
    servings := 0
    mutex := Mutex()
    mutex2 := Mutex()
    full_pot := Semaphore(0)
    empty_pot := Semaphore(0)
    barrier := SimpleBarrier()
    barrier2 := SimpleBarrier()

    for savage_id in [0, 1, 2, ..., N-1]:
        create_and_run_thread(savage, savage_id)
    for cook_id in [0, 1, ..., C-1]:
        create_and_run_thread(cook, cook_id)


def savage(savage):
    sleep(10 ms - 1s)
    while True:
        barrier1.wait()
        barrier2.wait()
        mutex.lock()
        if servings == 0:
            print("savage %2d: empty pot" % savage)
            empty_pot.signal(M)
            full_pot.wait()
        print("savage %2d: taking from pot" % savage)
        servings -= 1
        mutex.unlock()
        eat(savage)
        

def eat(savage):
    print("savage %2d eating" % savage)
    sleep(0,5 - 2 s)
    

def cook(cook):
    while True:
        empty_pot.wait()
        mutex2.lock()
        if servings < M:
            print("cook %2d: cooking" % cook)
            sleep(100 - 500ms)
            servings += 1
            if servings == M:
                full_pot.signal()
        mutex2.unlock()
```

Synchronization tools:

```
class Shared:
    """
    Class holding all the synchronization tools
    servings - servings remaining in the pot
    mutex - mutex for savages
    mutex2 - mutex for cooks
    empty_pot - signals empty pot
    full_pot - signals full pot
    barrier, barrier2 - barriers for savages
    """
    def __init__(self):
        self.servings = 0
        self.mutex = Mutex()
        self.mutex2 = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.barrier = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)
```

Implementation of multiple cooks meant modification of original cook method (as shown in pseudocode) and adding additional mutex to shared synchronization tools.

Cook method:

```
while True:
    shared.empty_pot.wait()
    shared.mutex2.lock()
    if shared.servings < M:
        print(f'cook {i}: cooking')
        sleep(randint(1, 5)/10)
        shared.servings += 1
        if shared.servings == M:
            shared.full_pot.signal()
    shared.mutex2.unlock()
```

Cooks wait until savage signals that the pot is empty - 0 servings remaining. Once they were woken up,
they check whether there is space for another serving, and if there is, they cook one. Each cook makes a serving independently.
Once the serving is cooked, cook checks whether the pot is full and if is, it signals savages to gather and start eating.

File: savages.py
