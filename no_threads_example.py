
from signal import signal, setitimer, ITIMER_REAL, SIGALRM
from threading import RLock

import time

TIMER_FREQUENCY = 0.5

_LOCK = RLock()
counter = 0

def continuous_counting():
    global counter
    while True:
        _LOCK.acquire()
        try:
            counter += 1
        finally:
            _LOCK.release()
        time.sleep(0.2)


def signal_handler(signum, frame):
    _LOCK.acquire()
    try:
        print(f"signal handler has lock")
    finally:
        _LOCK.release()



signal(SIGALRM, signal_handler)

setitimer(ITIMER_REAL, TIMER_FREQUENCY, TIMER_FREQUENCY)

continuous_counting()
