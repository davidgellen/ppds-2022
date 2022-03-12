from random import randint
from fei.ppds import Mutex, Semaphore, Thread, Event, print
from time import sleep


class Lightswitch:
    """
    Lightswitch class, implemented in week 3 assignment
    """
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        self.mutex.lock()
        self.counter = self.counter - 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


def init():
    access_data = Semaphore(1)
    turn = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_receptor = Lightswitch()
    valid_data = Event()

    for monitor_id in range(8):
        Thread(monitor, monitor_id, valid_data, turn, ls_monitor, access_data)

    for receptor_id in range(3):
        Thread(receptor, receptor_id, turn, ls_receptor, valid_data, access_data)


def monitor(monitor_id, valid_data, turn, ls_monitor, access_data):
    valid_data.wait()
    while True:
        turn.wait()
        reading_receptors_count = ls_monitor.lock(access_data)
        read_duration = randint(40, 50) / 1000
        turn.signal()
        print(f'monit "{monitor_id:02d}": '
              f'pocet_citajucich_monitorov={reading_receptors_count:02d},'
              f'trvanie_citania={read_duration:5.3f}')
        ls_monitor.unlock(access_data)


def receptor(receptor_id, turn, ls_receptor, valid_data, access_data):
    while True:
        sleep(randint(50, 60) / 1000)
        turn.wait()
        writing_receptors_count = ls_receptor.lock(access_data)
        if receptor_id < 2:
            write_duration = randint(10, 20) / 1000
        else:
            write_duration = randint(20, 25) / 1000
        turn.signal()

        print(f'cidlo "{receptor_id:02d}": pocet_zapisujucich_cidiel={writing_receptors_count:02d}, ' +
              f'trvanie_zapisu={write_duration:5.3f}')
        sleep(write_duration)
        valid_data.signal()
        ls_receptor.unlock(access_data)


if __name__ == '__main__':
    init()
