# Assignment 8
Create a simple application - both synchronous and asynchronous version.
The implementation is based on lecture https://www.youtube.com/watch?v=ZoUPTSNcNWM by Mgr. Ing. Matúš Jókay, PhD. and from website https://uim.fei.stuba.sk/i-ppds/8-cvicenie-asynchronne-programovanie/.

### Application concept
Application holds queue of a single number. 2 tasks will be accessing the number, waiting (sleeping) for the value of the number and passing the number - 1 back to the queue. The application will play a sound each time the application is done sleeping. Once the delay reaches 1 second, no more numbers shall be added to the queue and a sound indicating end for program will be played

To play a sound, we have to provide a sample and use method playsound from module playsound.

Sound sources: https://milujempracu.sk/11.mp3, https://milujempracu.sk/15.mp3
### Synchronous version:
Task:
```
def task(name, work_queue):
    if work_queue.empty():
        print(f"Task {name} nothing to do")
        try:
            playsound('15.mp3')
        except PlaysoundException:
            pass
    else:
        while not work_queue.empty():
            count = work_queue.get()
            if count != 1:
                work_queue.put(count - 1)
            print(f"Task {name} running, current count {count}")
            sleep(count)
            try:
                playsound('11.mp3')
            except PlaysoundException:
                pass
```

Main program:
```
def main():
    work_queue = queue.Queue()
    for work in [6]:
        work_queue.put(work)
    start_time = time.perf_counter()
    tasks = [(task, "One", work_queue), (task, "Two", work_queue)]
    for t, n, q in tasks:
        t(n, q)
    elapsed = time.perf_counter() - start_time
    print(f"elapsed time {elapsed}")
```
Synchronous implementation uses sleep method from time module, therefore the code is unable to work asynchronously.

Passing in value 6 to the queue, the time to complete the routine was 28.5 seconds.

file: synch.py
### Asynchronous version:
Task:
```
async def task(name, queue):
    while not queue.empty():
        delay = await queue.get()
        if delay != 1:
            await queue.put(delay - 1)
        print(f"Task {name} running")
        time_start = time.perf_counter()
        await asyncio.sleep(delay)
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time: {elapsed:.1f}")
        try:
            playsound('11.mp3')
        except PlaysoundException:
            pass
```

Main program:
```
async def main():
    work_queue = asyncio.Queue()
    for work in [6]:
        await work_queue.put(work)

    start_time = time.perf_counter()
    await asyncio.gather(
        task("One", work_queue),
        task("Two", work_queue),
    )
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed:.1f}")
    try:
        playsound('15.mp3')
    except PlaysoundException:
        pass
```
The asynchronous version uses the asyncio module. Accessing the queue requires using await, both getting and putting elements inside.

Passing in value 6 to the queue, the time to complete the routine was 13.2 seconds.

Naturally, the asynchronous version runs much faster since basically arguments (n, n - 1) are being processed at the same time. The time difference would be greater with bigger first number in the queue.

file: asynch.py