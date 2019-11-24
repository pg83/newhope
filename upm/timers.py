import threading
import random
import time
import sys


@y.singleton
def queue():
    store = {}
    q = y.queue.SimpleQueue()

    def step():
        def iter_new():
            while True:
                try:
                    yield q.get(True, 0.1)()
                except y.queue.Empty:
                    break

                try:
                    yield q.get_nowait()()
                except y.queue.Empty:
                    break

        for x in iter_new():
            k = int(random.random() * 1000000000000)
            store[k] = x

        ready = []
        deadline = time.time()

        for k, v in store.items():
            if v['d'] < deadline:
                ready.append(k)
                
        for k in ready:
            store.pop(k)['f']()

    def raise_exit():
        raise SystemExit(0)
    
    @y.signal_channel.read_callback()
    def done_timers(arg):
        if arg['signal'] == 'DOWN' and 'when' in arg:
            q.put(raise_exit)
            
        if arg['signal'] == 'INT':
            q.put(raise_exit)

    def read():
        while True:
            step()

    t = threading.Thread(target=read)
    t.start()

    return q


def super_sleep(f, t):
    queue().put(lambda: {'f': f, 'd': t + time.time()})


def run_by_timer(t):
    def wrapper(f):
        def func():
            f()
            super_sleep(func, t)

        func()

        return func

    return wrapper
