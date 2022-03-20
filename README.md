# Week 4

The implementation is a modification of source code from lecture's webpage https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-%f0%9f%9a%ac/ and lecture https://www.youtube.com/watch?v=iotYZJzxKf4

## Smokers:

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

## Powerplant 2:

Powerplant has 3 receptors, which keep updating measured values. Values are stored in shared space, each receptor having it' s own storage space within the mutual one.

Receptors update values every 50 - 60 ms, while the update itself takes 2 receptors 10 - 20 ms and 1 receptor 20 - 25 ms.

Powerplant also employs 8 operators, each one watching corresponding monitor showing measured values from the receptors. Update from receptors keeps getting requested, while update takes 40 - 50 ms. These monitors may start working only once all the receptors have sent their first measures.

### Pseudocode:

```
def init():
    access_data = Semaphore(1)
    turn = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_receptor = Lightswitch()
    valid_data = Event()

    for monitor_id in (0, 8):
        create_and_run_thread(monitor, monitor_id)

    for receptor_id in (0, 3):
        create_and_run_thread(receptor, receptor_id)

def monitor(monitor_id):
    valid_data.wait()
    while True:
        turniket.wait()
        reading_receptors_count = ls_monitor(access_data).lock()
        sleep(40 - 50 ms)
        turn.signal()
        print(f'monit "{monitor_id:02d}": '
              f'pocet_citajucich_monitorov={reading_receptors_count:02d},'
              f'trvanie_citania={read_duration:5.3f}')
        ls_monitor(access_data).unlock()

def receptor(receptor_id):
    while True:
        sleep(50 - 60 ms)
        turn.wait()
        writing_receptors_count = ls_receptor(access_data).lock()
        // 2 receptors take 10 - 20 ms, one takes 20 - 25 ms to update
        if receptor_id < 2:
            write_duration = (10 - 20 ms)
        else:
            write_duration = (20 - 25 ms)
        turn.signal()
        
        print(f'cidlo "{receptor_id:02d}": pocet_zapisujucich_cidiel={writing_receptors_count:02d}, ' +
              f'trvanie_zapisu={write_duration:5.3f}')        
        sleep(write_duration)
        valid_data.signal()
        ls_cidlo(accessData).unlock()
```
We print values in slovak language as stated in the assignment.

Used lightswitch is from last week' s assignment. Both monitors and receptors have their own lightswitch to keep track of active routines (currently updating).

Valid data keeps track of whether all receptors have already sent out values so that monitors can start their routine.

Everything needs to go through turnstile first, while going through we keep track of current count of same objects (monitors, receptors) currently updating.

File: Powerplant2.py