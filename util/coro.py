ic = y.inc_counter()

import time
import queue
import collections as cc
import os
import sys
import collections.abc
import random
import heapq
import threading


NOV = '$'


def set_name(func, name):
    func.__name__ = name

    return func

        
class AddPop(object):
    def pop(self):
        t = y.TOut()
        
        while (res := self.try_pop()) == NOV:
            if t.current() > 0:
                time.sleep(t.current())
                
            t.bad() 

        return res

    
class MTQ(object):
    def __init__(self, k=queue.SimpleQueue):
        self.q = k()

    def push(self, v):
        self.q.put(v)

    def pop(self):
        return self.q.get()

    def try_pop(self):
        try:
            return self.q.get_nowait()
        except queue.Empty:
            return NOV

        
class PQ(object):
    def __init__(self):
        self.r, self.w = y.os.pipe()

    def push(self, v):
        y.os.write(self.w, y.struct.pack('I', v))

    def pop(self):
        return y.struct.unpack('I', y.os.read(self.r, 4))[0]
    

class LFQ(AddPop):
    def __init__(self):
        self.q = [cc.deque() for i in range(0, 3)]

    def push(self, v):
        y.random.choice(self.q).append(v)

    def try_pop(self):
        q = [x for x in self.q]
        y.random.shuffle(q)
        
        for i in q: 
            try:
                return i.popleft()
            except IndexError:
                pass

        return NOV


def factory(where):
    if where == 'timer':
        return MTQ

    if where == 'sched':
        return MTQ


def nope():
    pass
    

@y.singleton
def is_debug():
    return 'debug' in y.config.get('coro', '')


def gen_int_uid():
    return int(random.random() * 100000000000)


class SchedAction(collections.abc.Awaitable):
    def __str__(self):
        return '<sched ' + self.name + ', from loop ' + str(self.loop) + ', action ' + self.action.__name__ + ', ' + str(self.id) + '>'

    def __repr__(self):
        return str(self)
    
    def __await__(self):
        yield self

    __iter__ = __await__

    def __init__(self, loop, name, action):
        self.id = ic()
        self.loop = loop
        self.name = name
        self.action = action

    def sched_action(self, **kwargs):
        return self.__dict__.pop('action')(**kwargs)
        
        
class Future(collections.abc.Awaitable):
    def __str__(self):
        return '<fut ' + self.name + ', from loop ' + str(self.loop) + ', ' + str(self.id) + '>'

    def __repr__(self):
        return str(self)
    
    def __await__(self):
        yield self
        return self.result()

    __iter__ = __await__

    def __init__(self, loop, action):
        self.id = ic()
        self.cb = []
        self.loop = loop
        self.name = 'fut_' + action.__name__
        self.action = action
        
    @property
    def __name__(self):
        return self.name
        
    def signal(self):
        self.set_result(None)
        
    def set_result(self, res):
        self.run_job(lambda: res)
        
    def run_job(self, job):
        self.r = y.sync_pack(job)
        self.call_all_callbacks()
        
    def result(self):
        try:
            return y.unpack(self.r)
        except AttributeError:
            return self

    def run_action(self):
        self.pop('action', nope)()
        
    def add_cb(self, cb):
        self.cb.append(cb)
        self.run_action()
            
    def is_done(self):
        try:
            self.r

            return True
        except AttributeError:
            return False

    @property
    def pop(self):
        return self.__dict__.pop
        
    def call_all_callbacks(self):
        for c in self.pop('cb'):
            c()

    def sched_action(self, coro, **kwargs):
        self.add_cb(set_name(lambda: self.loop.reschedule(coro), 'reschedule_' + coro.name))

    
class MinHeap(object):
    def __init__(self):
        self.v = []

    def pack(self, key, val):
        return (key, gen_int_uid(), val)

    def unpack(self, x):
        return (x[0], x[2])

    def push(self, k, v):
        heapq.heappush(self.v, self.pack(k, v))

    def pop(self):
        return self.unpack(heapq.heappop(self.v))
        
    def min_element(self):
        return self.unpack(self.v[0])

    def pop_smallest(self, maxk):
        while self.v:
            mink, v = self.min_element()

            if mink <= maxk:
                yield self.pop()
            else:
                return

    def min_key(self):
        return self.min_element()[0]

    def empty(self):
        return not self.v
    

class Scheduler(object):
    def get_next(self):
        pass

    def reschedule(self, c):
        pass

    
class SimpleRR(Scheduler):
    def __init__(self):
        self.d = factory('sched')()

    async def get_next(self):
        return COROS[self.d.pop()]

    def reschedule(self, v):
        self.d.push(v.id)


class ReadFile(object):
    def __init__(self, name, loop):
        self.loop = loop
        self.name = name
        self.f = None
        
    async def open(self):
        self.f = await loop.offload(set_name(lambda: open(self.name, 'rb'), 'open_file'))

    async def close(self):
        await loop.offload(self.f.close)
        self.f = None
        
    async def read(self):
        assert self.f
        return await loop.offload(self.f.read)
    
    async def read_line(self):
        assert self.f
        return await loop.offload(self.f.readline)

    
class TimeScheduler(object):
    def __init__(self, loop, name):
        self.loop = loop
        self.name = name
        self.h = MinHeap()

    @property
    def tq(self):
        return self.loop.timer_queue
        
    def add(self, deadline, cb):
        self.h.push(deadline, cb)

    def iter_next(self):
        return list(self.h.pop_smallest(time.time()))

    def next_deadline(self):
        return self.h.min_key()

    def empty(self):
        return self.h.empty()

    async def sleep(self, tout):
        return await self.sleep_deadline(time.time() + tout)

    async def sleep_deadline(self, dd):
        return await self.loop.offload(set_name(lambda: time.sleep(max(dd - time.time(), 0.001)), 'sleep_' + str(int(dd))))
        
    async def wait_queue(self):
        self.process_queue()

        tout = y.TOut()
        
        while self.empty():
            if tout.current() > 0:
                await self.sleep(tout.current())

            tout.bad()

            self.process_queue()
            
    async def step(self):
        await self.wait_queue()
        await self.sleep_deadline(self.next_deadline())

        for d, cb in self.iter_next():
            cb()

    def process_queue(self):
        while (val := self.tq.try_pop()) != NOV:
            self.add(*val)
            
    async def system_time_checker(self, ctl):
        while True:
            try:
                await self.step()
            except GeneratorExit:
                self.respawn()
                is_debug() and y.debug('generator exit, respawn')

                return
            except Exception:
                y.on_except()

    def respawn(self):
        self.loop.spawn(self.system_time_checker, self.name)

        
COROS = {}

                
class Coro(collections.abc.Coroutine):
    def __init__(self, loop, coro, name):
        self.id = ic()
        self.n = name
        self.c = coro
        self.l = loop
        self.f = self.create_future(nope)
        self.r = self.c(self)
        self.s = y.collections.deque()
        self.v = None

        COROS[self.id] = self
        
    def __str__(self):
        state = str(y.inspect.getcoroutinestate(self))[5:].lower()
        
        return '<coro ' + self.name + ', from ' + str(self.loop) + ', ' + state + ', ' + str(self.id) + '>'

    def __repr__(self):
        return str(self)
    
    def is_system(self):
        return 'system_' in self.name

    @property
    def name(self):
        return self.n

    @property
    def __name__(self):
        return self.name
    
    @property
    def slave(self):
        return self.r
        
    @property
    def loop(self):
        return self.l

    def result(self):
        return self.v
    
    def step_0(self):
        try:
            if self.is_system():
                return self.slave.send(None)

            try:
                is_debug() and y.debug(str(self), 'step in')
                
                return self.slave.send(None)
            finally:
                is_debug() and y.debug(str(self), 'step out')
        except StopIteration as e:
            is_debug() and y.debug(str(self), 'here we are', e, 'with result', e.value)
            
            self.v = e.value
            self.f.set_result(self)

            raise

    def step(self):
        try:
            return self.step_0()
        except StopIteration:
            raise
        except:
            y.os.abort()

    def next(self):
        return next(self)

    def reschedule(self):
        self.l.reschedule(self)
    
    def send(self, v):
        y.os.abort()
        return self.slave.send(v)
    
    def throw(self, *args):
        return self.slave.throw(*args)
        
    def close(self):
        return self.slave.close()
        
    def __await__(self):
        return self.f.__await__()

    def __iter__(self):
        return self

    def __next__(self):
        return self.step()
        
    def spawn(self, c, name=None):
        name = name or c.__name__
        res = self.l.spawn(c, self.name + '_' + name)
        
        self.s.append(res)

        return res
                
    def create_future(self, action):
        return self.l.create_future(action)

    def create_sched_action(self, action):
        return self.l.create_sched_action(action)

    def create_yield(self):
        return self.l.create_yield()

    async def sched_yield(self):
        return await self.l.sched_yield()
    
    async def sleep(self, tout):
        return await self.l.sleep(tout)
    
    async def sleep_deadline(self, d):
        return await self.l.sleep_deadline(d)
    
    def await_sync(self):
        while True:
            try:
                return self.f.result()
            except AttributeError:
                pass

            time.sleep(0.01)

    @property
    def cr_await(self):
        return self.slave.cr_await

    @property
    def cr_code(self):
        return self.slave.cr_code

    @property
    def cr_frame(self):
        return self.slave.cr_frame

    @property
    def cr_origin(self):
        return self.slave.cr_origin

    @property
    def cr_running(self):
        return self.slave.cr_running

    
class Loop(object):
    def __init__(self, name, scheduler=None):
        self.name = name
        self.sched = scheduler or SimpleRR()
        self.timer_queue = factory('timer')()
        self.timers = [TimeScheduler(self, 'system_tc_' + str(i)) for i in range(0, 10)]
        self.thrs = [y.threading.Thread(target=self.drive) for i in range(0, 20)]

        for t in self.thrs:
            t.start()

        for t in self.timers:
            t.respawn()
        
    def __str__(self):
        return '<loop ' + self.name + '>'

    def __repr__(self):
        return str(self)
    
    async def read_file(self, name):
        rf = ReadFile(name, loop)

        await rf.open()

        if rf.f:
            return rf

        raise Exception('can not open file ' + name)
    
    def schedule(self, coro, name):
        res = Coro(self, coro, name)

        self.sched.reschedule(res)
        is_debug() and y.debug('spawn', str(res))
        
        return res

    def spawn(self, coro, name=None):
        name = name or coro.__name__
        
        return self.schedule(coro, name)
    
    def reschedule(self, coro):    
        self.sched.reschedule(coro)

        if is_debug():
            if not coro.is_system():
                y.debug('reschedule', str(coro))

    async def one_step(self):
        c = await self.sched.get_next()
        
        try:
            x = c.next()
        except StopIteration:
            return
    
        if x:
            return x.sched_action(loop=self, coro=c)

        self.reschedule(c)

    async def drive_async(self):
        while True:
            await self.one_step()
            
    def drive(self):
        async def main(ctl):
            return await self.drive_async()
        
        c = Coro(self, main, 'main')

        while True:
            try:
                x = c.next()
            except StopIteration as e:
                return e.value
    
            if x:
                x.sched_action(loop=self, coro=c)

    async def sched_yield(self):
        return await self.create_yield()
        
    def create_yield(self):
        def yield_action(loop, coro):
            loop.reschedule(coro)
        
        return self.create_sched_action(yield_action)
        
    def create_sched_action(self, action):
        return SchedAction(self, self.name + '_' + action.__name__, action)
    
    def create_future(self, action):
        return Future(self, action)
        
    async def sleep_deadline(self, dd):
        name = 'sleep_deadline_' + str(int(dd))
        fut = self.create_future(set_name(lambda: self.timer_queue.push((dd, fut.signal)), name))

        return await fut
        
    async def sleep(self, tout):
        if tout < 0.015:
            return await self.sched_yield()
        
        t1 = time.time()
        
        try:
            return await self.sleep_deadline(t1 + tout)
        finally:
            is_debug() and y.debug('sleep for', time.time() - t1, tout)

    async def offload(self, job):
        async def async_job(ctl):
            return y.sync_pack(job)

        return y.unpack((await self.spawn(async_job, 'async_' + job.__name__)).__dict__.pop('v'))

    async def map(self, func, data):
        def gen_func(el):
            async def async_func(ctl):
                return await func(el)

            return async_func

        h = [self.spawn(gen_func(el)) for el in data]
        r = [await x for x in h]

        return r

    
async_loop = Loop('main')
