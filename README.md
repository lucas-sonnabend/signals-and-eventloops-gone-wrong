
# Signals and Eventloop going wrong

This is a small repository to reproduce this error:
```
RuntimeError: cannot release un-acquired lock
```

It is based on an actual bug I saw in production systems, it took some time to debug,
and the explanation is quite interesting. [You can read more in the article here](https://betterprogramming.pub/how-i-solved-a-challenging-concurrency-bug-in-python-cbf635d4bea9?sk=9eea8d7c854c052485e6a58afe0d41b7).

## Getting started 

### requirements

You will need to have python and [poetry](https://python-poetry.org/docs/#installation) installed on your system.

### installing the dependencies

To install the python dependencies run
```bash
$ poetry install
```

### run the examples

To execute the example run
```bash
$ poetry run gevent_example.py
```

Eventually you will see one of the following exceptions on the console. The first one will stop the program, and happen eventually, within seconds, but it can take up to a minute.

```
Traceback (most recent call last):
  File "gevent_example.py", line 41, in <module>
    thread.join()
  File "src/gevent/greenlet.py", line 831, in gevent._gevent_cgreenlet.Greenlet.join
  File "src/gevent/greenlet.py", line 857, in gevent._gevent_cgreenlet.Greenlet.join
  File "src/gevent/greenlet.py", line 846, in gevent._gevent_cgreenlet.Greenlet.join
  File "src/gevent/_greenlet_primitives.py", line 61, in gevent._gevent_c_greenlet_primitives.SwitchOutGreenletWithLoop.switch
  File "src/gevent/_greenlet_primitives.py", line 61, in gevent._gevent_c_greenlet_primitives.SwitchOutGreenletWithLoop.switch
  File "src/gevent/_greenlet_primitives.py", line 65, in gevent._gevent_c_greenlet_primitives.SwitchOutGreenletWithLoop.switch
  File "src/gevent/_gevent_c_greenlet_primitives.pxd", line 35, in gevent._gevent_c_greenlet_primitives._greenlet_switch
gevent.exceptions.LoopExit: This operation would block forever
	Hub: <Hub '' at 0x7f4ffacb6ac0 epoll default pending=0 ref=0 fileno=3 thread_ident=0x7f4ffffda180>
	Handles:
[]
```

The other two are more rare, you might see them every 10 runs, althouh I haven't collected enough samples to have high confidency in this frequency.
They also don't halt the program.

```
Traceback (most recent call last):
  File "src/gevent/greenlet.py", line 906, in gevent._gevent_cgreenlet.Greenlet.run
  File "gevent_example2.py", line 21, in continuous_print
    _LOCK.release()
  File "/home/lucas/.pyenv/versions/3.8.5/lib/python3.8/threading.py", line 179, in release
    raise RuntimeError("cannot release un-acquired lock")
RuntimeError: cannot release un-acquired lock
2021-09-13T19:31:17Z <Greenlet at 0x7fac5ae05040: continuous_print(2)> failed with RuntimeError
```


```
Traceback (most recent call last):
  File "src/gevent/greenlet.py", line 906, in gevent._gevent_cgreenlet.Greenlet.run
  File "gevent_example.py", line 20, in continuous_counting
    _LOCK.release()
  File "/home/lucas/.pyenv/versions/3.8.5/lib/python3.8/threading.py", line 183, in release
    self._block.release()
  File "src/gevent/_semaphore.py", line 496, in gevent._gevent_c_semaphore.BoundedSemaphore.release
  File "src/gevent/_semaphore.py", line 502, in gevent._gevent_c_semaphore.BoundedSemaphore.release
RuntimeError: Semaphore released too many times
2021-09-13T20:13:40Z <Greenlet at 0x7f2a76d7ebf0: continuous_counting(0)> failed with RuntimeError
```
