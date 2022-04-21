import queue
from playsound import playsound, PlaysoundException
from time import sleep
import time


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


if __name__ == "__main__":
    main()
