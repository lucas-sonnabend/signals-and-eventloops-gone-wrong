from gevent import monkey
monkey.patch_all()
from gevent import spawn, sleep
from signal import signal, setitimer, ITIMER_REAL, SIGALRM
from threading import RLock
from sys import stdout


TIMER_FREQUENCY = 1

_LOCK = RLock()
counter = 0

def continuous_print(thread_name):
    global counter
    while True:
        _LOCK.acquire()
        try:
            counter += 1
        finally:
            _LOCK.release()
        sleep(0)


def signal_handler(signum, frame):
    _LOCK.acquire()
    try:
        print(f"signal handler has lock")
        pass
    finally:
        _LOCK.release()



signal(SIGALRM, signal_handler)

setitimer(ITIMER_REAL, TIMER_FREQUENCY, TIMER_FREQUENCY)

threads = [spawn(continuous_print, i) for i in range(5)]

for thread in threads:
    thread.join()


