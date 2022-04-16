import asyncio
import time


async def task(name, queue):
    while not queue.empty():
        delay = await queue.get()
        print(f"Task {name} running")
        time_start = time.perf_counter()
        await asyncio.sleep(delay)
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time: {elapsed:.1f}")


async def main():
    work_queue = asyncio.Queue()
    for work in [15, 10, 5, 2]:
        await work_queue.put(work)
    start_time = time.perf_counter()
    await asyncio.gather(
        task("One", work_queue),
        task("Two", work_queue),
    )
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed:.1f}")


if __name__ == "__main__":
    asyncio.run(main())
