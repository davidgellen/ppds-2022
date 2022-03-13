# Week 4

Assignment furthermore explores concepts from last week. The implementation is a modification of source code from lecture's webpage https://uim.fei.stuba.sk/i-ppds/4-cvicenie-vecerajuci-filozofi-atomova-elektraren-%f0%9f%8d%bd%ef%b8%8f/ and concepts from seminar from 09/03/2022.

## Powerplant 1:

Powerplant has 11 receptors and 2 monitors. 

Receptors keep trying to update measured values to shared space. Each updates takes 10 - 15 ms.

Monitors show current values measured. They send request for update from receptors each 500 ms after finishing the last update. 
Each update has to finish in 200 ms. 

Monitors can only start working after at least one receptor has sent data to it.

This task was explained on lecture, pseudocode can be found on website. The task was to do the implementation.

File: Powerplant1.py

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