
import asyncio
from signal import signal, setitimer, ITIMER_REAL, SIGALRM
from threading import RLock

TIMER_FREQUENCY = 2

_LOCK = RLock()
counter = 0

async def continuous_counting():
    global counter
    while True:
        _LOCK.acquire()
        try:
            counter += 1
        finally:
            _LOCK.release()
        await asyncio.sleep(0)


def signal_handler(signum, frame):
    _LOCK.acquire()
    try:
        print(f"signal handler has lock")
    finally:
        _LOCK.release()



signal(SIGALRM, signal_handler)

setitimer(ITIMER_REAL, TIMER_FREQUENCY, TIMER_FREQUENCY)

async def main():
    await asyncio.gather(
        continuous_counting(), continuous_counting(), continuous_counting()
    )

asyncio.run(main())
