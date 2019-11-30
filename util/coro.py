import time
import queue
import collections as cc
import os
import sys
import collections.abc
import random
import heapq
import threading


NOV = 'sentinel'


class AddPop(object):
    def pop(self):
        t = 0.01
        res = NOV
        
        while res == NOV:
            res = self.try_pop()

            if res != NOV:
                return res
            
            time.sleep(t)
            t = min(t * 1.2 + 0.01, 0.2)    
    

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
        

class LFQ(AddPop):
    def __init__(self):
        self.q = cc.deque()

    def push(self, v):
        self.q.append(v)

    def try_pop(self):
        try:
            return self.q.popleft()
        except IndexError:
            return NOV

        
class SQ(AddPop):
    def __init__(self):
        self.l = threading.Lock()
        self.q = cc.deque()

    def push(self, v):
        with self.l:
            self.q.append(v)

    def try_pop(self):
        with self.l:
            try:
                return self.q.popleft()
            except IndexError:
                return NOV
            

def factory(where):
    if where == 'timer':
        return LFQ

    if where == 'sched':
        return LFQ

    if where == 'async':
        return LFQ

    if where == 'offload':
        return MTQ
    
    
@y.singleton
def is_dbg():
    return '/debug/coro' in y.verbose


def is_debug(val=False):
    return val or is_dbg()


def gen_int_uid():
    return int(random.random() * 10000000000000000000000000)

        
class FutureHolder(object):
    def __init__(self, fut, coro):
        self.fut = fut
        self.coro = coro

    def run(self):
        self.fut.loop.reschedule(self.coro)


class Future(collections.abc.Awaitable):
    def __str__(self):
        return '<future ' + self.name + ', from loop ' + str(self.loop) + '>'

    def __repr__(self):
        return str(self)
    
    def future_holder(self, fut, coro):
        return FutureHolder(fut, coro)
    
    def __await__(self):
        yield self
        return self.result()

    __iter__ = __await__

    def __init__(self, loop, name):
        self.cb = []
        self.loop = loop
        self.name = name

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
        
    def add_cb(self, cb):
        self.cb.append(cb)

    def is_done(self):
        try:
            self.r

            return True
        except AttributeError:
            return False
        
    def call_all_callbacks(self):
        try:
            for c in self.cb:
                c()
        finally:
            self.cb = []

    
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
        return c

    
class SimpleRR(Scheduler):
    def __init__(self):
        self.d = factory('sched')()
        
    def get_next(self):
        return self.d.pop()

    def reschedule(self, v):
        self.d.push(v)
        return v


class ReadFile(object):
    def __init__(self, name, loop):
        self.loop = loop
        self.name = name
        self.f = None
        
    async def open(self):
        self.f = await loop.offload(lambda: open(self.name, 'rb'))

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

    @property
    def sleep_deadline(self):
        return self.loop.sleep_deadline_0
        
    async def wait_queue(self):
        self.process_queue()

        while self.empty():
            await self.sleep(0.1)
            self.process_queue()
            
    async def step(self):
        await self.wait_queue()
        await self.sleep_deadline(self.next_deadline())

        for d, cb in self.iter_next():
            cb()

    def process_queue(self):
        while True:
            val = self.tq.try_pop()
            
            if val == NOV:
                return
            
            self.add(*val)
            
    async def system_time_checker(self, ctl):
        while True:
            try:
                await self.step()
            except GeneratorExit:
                is_debug() and y.debug('generator exit, respawn')
                self.respawn()

                return
            except Exception:
                y.on_except()

    def respawn(self):
        self.loop.spawn(self.system_time_checker, self.name)
                
                
class Coro(collections.abc.Coroutine):
    def __init__(self, loop, coro, name):
        self.n = name
        self.c = coro
        self.l = loop
        self.f = self.create_future('await_' + self.name)
        self.r = self.c(self)
        self.s = y.collections.deque()
        self.v = None

    def __str__(self):
        return '<coro ' + self.name + ', from ' + str(self.loop) + ', ' + str(y.inspect.getcoroutinestate(self))[5:].lower() + '>'

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
            is_debug() and y.debug(str(self), 'here we are', e)
            is_debug() and y.debug(str(self), 'done', 'with result', e.value)
            
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
        
    def spawn(self, c, name):
        res = self.l.spawn(c, self.name + '_' + name)
        self.s.append(res)

        return res
                
    def create_future(self, name):
        return self.l.create_future(self.name + '_' + name)
    
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

            time.sleep(0.1)

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
        self.timers = [TimeScheduler(self, 'system_tc_' + str(i)) for i in range(0, 3)]
        self.q = factory('offload')()
        self.thrs = [y.threading.Thread(target=self.system_queue_runner) for i in range(0, 20)]

        for t in self.thrs:
            t.start()

        for i in range(0, 5):
            self.q.push(self.drive)

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
        
    def next_ready(self):
        return self.sched.get_next()
    
    def schedule(self, coro, name):
        res = Coro(self, coro, name)

        is_debug() and y.debug('spawn', str(res))
        self.sched.reschedule(res)
        
        return res

    def spawn(self, coro, name):
        return self.schedule(coro, name)
    
    def reschedule(self, coro):
        if not coro.is_system():
            is_debug() and y.debug('reschedule', str(coro))
            
        self.sched.reschedule(coro)

    def one_step(self):
        c = self.next_ready()

        try:
            x = c.next()
        except StopIteration:
            return
    
        if x:
            if self.process_value(x, c):
                return
            else:
                is_debug() and y.debug('unprocessed value', x)

        self.reschedule(c)

    def process_value(self, x, c):
        klass_name = x.__class__.__name__.lower()

        if klass_name == 'future':
            return self.process_future(x, c)

        return False

    def create_future(self, name):
        return Future(self, self.name + '_' + name)

    async def sleep_deadline_0(self, dd):
        return await self.offload(lambda: time.sleep(max(dd - time.time(), 0.001)))
        
    async def sleep_deadline_1(self, dd):
        fut = self.create_future('sleep')
        self.timer_queue.push((dd, fut.signal))
        return await fut

    async def sleep_deadline(self, dd):
        return await self.sleep_deadline_1(dd)

    async def _yield(self):
        async def func(ctl):
            return 42

        return await self.spawn(func, 'yield_func')
        
    async def sleep(self, tout):
        t1 = time.time()
        
        try:
            return await self.sleep_deadline(t1 + tout)
        finally:
            is_debug() and y.debug('sleep for', time.time() - t1, tout)
         
    def process_future(self, fut, coro):
        fut.add_cb(fut.future_holder(fut, coro).run)

        return True

    def drive(self):
        while True:
            self.one_step()

    async def offload(self, job):
        fut = self.create_future('offload_' + job.__name__)
        self.q.push(lambda: fut.run_job(job))
        return await fut
                
    def system_queue_runner(self):
        while True:
            try:
                self.q.pop()()
            except Exception:
                y.on_except()

    async def map(self, func, data):
        def gen_func(el):
            async def async_func(ctl):
                return await func(el)

            return async_func

        h = [self.spawn(gen_func(el)) for el in data]
        r = [await x for x in h]

        return r

    
async_loop = Loop('main')
