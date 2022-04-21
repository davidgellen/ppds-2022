import asyncio
import time
from playsound import playsound, PlaysoundException


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


if __name__ == "__main__":
    asyncio.run(main())
