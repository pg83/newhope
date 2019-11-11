import threading
import Queue
import random
import time
import sys


@y.singleton
def queue():
    store = {}

    def step():
        def iter_new():
            while True:
                try:
                    yield q.get_nowait()()
                except Queue.Empty:
                    break

        for x in iter_new():
            k = int(random.random() * 1000000000000)
            store[k] = x

        ready = []
        deadline = time.time()

        for k, v in store.iteritems():
            if v['d'] > deadline:
                ready.append(k)
                
        for k in ready:
            store.pop(k)['f']()
            
    def read():
        while not y.main_thread_dead():
            time.sleep(0.1)
            step()

    t = threading.Thread(target=read)
    t.start()
    q = Queue.Queue()

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


@y.defer_constructor
def init():
   qq = y.homeland_queue

   @y.run_by_timer(0.15)
   def func_helper():
       def ff():
           pass

       qq.put(ff)
