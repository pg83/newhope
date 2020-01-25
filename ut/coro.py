import time
import queue
import collections as cc
import os
import sys
import collections.abc
import random
import heapq
import threading
import weakref
import contextvars as cv


CURRENT_CORO = cv.ContextVar('CURRENT_CORO')
NOV = '$'


def current_coro():
    return CURRENT_CORO.get()


@y.contextlib.contextmanager
def with_contextvar(coro):
    token = CURRENT_CORO.set(coro)

    try:
        yield
    finally:
        CURRENT_CORO.reset(token)


def wrap_context(func):
    @y.functools.wraps(func)
    def func1(self):
        with with_contextvar(self):
            return func(self)

    @y.functools.wraps(func)
    def wrapped(self):
        return self.ctx.run(func1, self)

    return wrapped


def set_name(func, name):
    func.__name__ = name

    return func


def factory(where):
    if where == 'timer':
        return y.MTQ


def nope():
    pass


@y.singleton
def is_dbg():
    return 'debug' in y.config.get('coro', '')


class X(object):
    debug = True


def is_debug(ctx=X):
    return ctx.debug and is_dbg()


def gen_int_uid():
    return int(random.random() * 100000000000)


class SchedAction(collections.abc.Awaitable):
    def __str__(self):
        return '<sched ' + self.name + ', from ' + self.loop_name + ', action ' + self.action.__name__ + ', ' + str(self.id) + '>'

    def __repr__(self):
        return str(self)

    def __await__(self):
        yield self

    __iter__ = __await__

    def __init__(self, id, loop_name, action):
        self.id = id
        self.loop_name = loop_name
        self.name = loop_name + '_' + action.__name__
        self.action = action

    def sched_action(self, coro):
        return self.__dict__.pop('action')(coro)


class Future(collections.abc.Awaitable):
    def __str__(self):
        return '<fut ' + self.name + ', from loop ' + self.ln + ', ' + str(self.id) + '>'

    def __repr__(self):
        return str(self)

    def __await__(self):
        yield self
        return self.result()

    __iter__ = __await__

    def __init__(self, id, loop_name, action):
        self.ln = loop_name
        self.id = id
        self.cb = []
        self.name = 'fut_' + action.__name__
        self.action = action

    @property
    def __name__(self):
        return self.name

    def signal(self):
        self.set_result([None])

    def set_result(self, res):
        self.run_job(lambda: res)

    def run_job(self, job):
        self.r = y.sync_pack(job)
        self.call_all_callbacks()

    def result(self):
        try:
            return y.unpack(self.r)
        except AttributeError:
            return None

    def add_cb(self, cb):
        self.cb.append(cb)

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

    def sched_action(self, coro):
        try:
            self.add_cb(coro.reschedule)
            self.pop('action')()
        except Exception as e:
            print e, str(coro), str(self), str(self.result())
            y.prompt('/sa')
            coro.reschedule()


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


class ReadFile(object):
    def __init__(self, name, loop):
        self.loop = loop
        self.name = name
        self.f = None

    async def open(self):
        self.f = await self.loop.offload(set_name(lambda: open(self.name, 'rb'), 'open_file'))

    async def close(self):
        await self.loop.offload(self.f.close)
        self.f = None

    async def read(self):
        assert self.f
        return await self.loop.offload(self.f.read)

    async def read_line(self):
        assert self.f
        return await self.loop.offload(self.f.readline)


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
        return await current_coro().loop.offload(set_name(lambda: time.sleep(max(dd - time.time(), 0)), 'sleep_' + str(int(dd))))

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

    async def system_time_checker(self):
        while True:
            await self.step()

    def respawn(self):
        self.loop.spawn(self.system_time_checker, self.name, debug=False)


COROS = {}


def coro_rescheduler(coro, i):
    coro.loop.loop.thrs[i].reschedule(coro)


def yield_action(coro):
    coro.reschedule()


class Green(object):
    def __init__(self, func, loop):
        self.f = func
        self.g = self.f(self)
        self.a = loop.create_future(nope)
        self.s = 'CREATED'
        self.cr_await = None

    def __pow__(self, other):
        self.cr_await = other

        try:
            yield from other.__await__()
        finally:
            self.cr_await = None

    def __await__(self):
        return self.a.__await__()

    def send(self, v):
        assert not self.is_closed()

        try:
            self.s = 'RUNNING'

            try:
                return self.g.send(v)
            finally:
                self.s = 'SUSPENDED'
        except StopIteration as e:
            self.s = 'CLOSED'
            self.a.set_result(e.value)

            raise e
        except:
            self.s = 'CLOSED'

            def func():
                raise

            self.a.run_job(func)

    def is_closed(self):
        return self.s == 'CLOSED'

    def throw(self, *args):
        assert not self.is_closed()

        self.g.throw(*args)

    def close(self):
        assert not self.is_closed()

        self.close()

    @property
    def __name__(self):
        return self.f.__name__

    @property
    def cr_code(self):
        return self.f.__code__

    @property
    def cr_frame(self):
        return self.g.gi_frame

    @property
    def cr_origin(self):
        return None

    @property
    def cr_running(self):
        return self.s
 

class Coro(collections.abc.Coroutine):
    def __init__(self, loop, coro, ctx, name, debug):
        if not y.inspect.iscoroutinefunction(coro):
            x = coro
            coro = lambda: Green(x, loop)

        self.debug = debug
        self.ctx = ctx

        try:
            self.id = current_coro().l.next_id()
        except LookupError:
            self.id = loop.next_id()

        self.n = name
        self.l = loop
        self.f = self.create_future(nope)
        self.change_state(coro)
        self.s = y.collections.deque()

        COROS[self.id] = self

    def change_state(self, coro):
        self.c = coro

        try:
            self.r = self.c(self)
        except TypeError:
            self.r = self.c()

    def __str__(self):
        state = str(y.inspect.getcoroutinestate(self))[5:].lower()

        return '<' + self.r.__class__.__name__.lower() + ' ' + self.name + ', ' + str(self.loop) + ', ' + state + ', id ' + str(self.id) + '>'

    def __repr__(self):
        return str(self)

    @property
    def thread_id(self):
        return self.loop.thread_id

    @property
    def thread_count(self):
        return self.loop.thread_count

    async def go_to_thread(self, i):
        assert i < self.thread_count
        assert i >= 0

        while self.thread_id != i:
            await self.sched_yield()
            await self.create_sched_action(set_name(lambda x: coro_rescheduler(x, i), 'coro_rescheduler_' + str(i)))

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
        return self.f.result()

    def step(self):
        try:
            return self.step_0()
        except StopIteration as e:
            COROS.pop(self.id)

            is_debug(self) and y.debug(str(self), 'here we are', e)

            self.f.set_result(e.value)

            raise

    @wrap_context
    def step_0(self):
        return self.slave.send(None)

    def next(self):
        return (self.step() or self.l).sched_action(self)

    def reschedule(self):
        self.l.reschedule(self)

    def send(self, v):
        y.os.abort()

    @wrap_context
    def throw(self, *args):
        return self.slave.throw(*args)

    @wrap_context
    def close(self):
        return self.slave.close()

    def __await__(self):
        return self.f.__await__()

    def spawn(self, coro, name=None, debug=None):
        if debug is None:
            debug = self.debug

        name = name or coro.__name__
        res = self.l.spawn_impl(coro, self, self.name + '_' + name, debug)

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


class ThreadLoop(object):
    def __init__(self, ctx, i, name, loop):
        self.next_id = y.inc_counter()
        self.ctx = ctx
        self.rng = y.PCGRandom(3, i)
        self.i = i
        self.name = name
        self.loop = loop
        self.q = cc.deque()
        self.t = y.threading.Thread(target=self.thr_loop)

    @property
    def thread_id(self):
        return self.i

    @property
    def thread_count(self):
        return len(self.loop.thrs)

    @property
    def int_random(self):
        return self.rng.next_random

    @property
    def float_random(self):
        return self.rng.next_float

    def __str__(self):
        return '<loop ' + self.name + '>'

    def __repr__(self):
        return str(self)

    def start(self):
        self.t.start()

    def thr_loop(self):
        try:
            self.ctx.run(self.drive_sync)
        except:
            y.os.abort()

    async def read_file(self, name):
        rf = ReadFile(name, self)

        await rf.open()

        if rf.f:
            return rf

        raise Exception('can not open file ' + name)

    def schedule(self, coro, ctx, name, debug):
        res = Coro(self, coro, ctx, name, debug)

        is_debug(res) and y.debug('spawn', str(res))
        self.reschedule(res)

        return res

    def spawn(self, coro, name=None, debug=True):
        return self.spawn_impl(coro, self, name, debug)

    def spawn_impl(self, coro, parent, name, debug):
        name = name or coro.__name__

        return self.schedule(coro, parent.ctx.copy(), name, debug)

    def reschedule(self, coro):
        coro.l = self
        self.q.append(coro.id)

        is_debug(coro) and y.debug('reschedule', str(coro))

    def iter_thrs1(self):
        if 0:
            while True:
                yield self.i
                time.sleep(0.001)

        for i in range(0, 20):
            yield self.i + i
            time.sleep(0)

        c = self.i

        while True:
            yield c

            time.sleep(0.001)

            c = c + 1 + 5 * self.float_random()

            if c > 1000:
                c = 0

    def get_next(self):
        tt = self.loop.thrs

        for j in self.iter_thrs1():
            try:
                c_id = tt[int(j) % len(tt)].q.popleft()
            except IndexError:
                continue

            c = COROS[c_id]
            c.l = self

            return c

    def one_step_sync(self, c): 
        try:
            return c.next()
        except StopIteration as s:
            return

    def sched_action(self, x):
        return self.reschedule(x)

    def drive_sync(self):
        while True:
            self.one_step_sync(self.get_next())
            time.sleep(0)

    async def sched_yield(self):
        return await self.create_yield()

    def create_yield(self):
        return self.create_sched_action(yield_action)

    def create_sched_action(self, action):
        return SchedAction(self.next_id(), self.name, action)

    def create_future(self, action):
        return Future(self.next_id(), str(self), action)

    async def sleep_deadline(self, dd):
        name = 'sleep_deadline_' + str(int(dd))
        fut = self.create_future(set_name(lambda: self.loop.timer_queue.push((dd, fut.signal)), name))

        return await fut

    async def sleep(self, tout):
        if tout < 0.02:
            return await self.sched_yield()

        t1 = time.time()

        try:
            return await self.sleep_deadline(t1 + tout)
        finally:
            is_debug() and y.debug('sleep for', time.time() - t1, tout)

    async def offload(self, job):
        async def async_job(ctl):
            return y.sync_pack(job)

        return y.unpack(await self.spawn(async_job, 'async_' + job.__name__, debug=('sleep' not in job.__name__)))


class CoroLoop(object):
    def __init__(self, name, scheduler=None):
        self.ctx = cv.copy_context()
        self.name = name
        self.timer_queue = factory('timer')(self)
        self.timers = [TimeScheduler(self, 'system_tc_' + str(i)) for i in range(0, 5)]
        self.thrs = [ThreadLoop(self.ctx.copy(), i, name + '_' + str(i), self) for i in range(0, 20)]

        for t in self.thrs:
            t.start()

        for t in self.timers:
            t.respawn()

        #self.spawn(self.collect_stats)

    def __str__(self):
        return '<loop ' + self.name + '>'

    def __repr__(self):
        return str(self)

    async def collect_stats(self):
        cc = y.current_coro()

        while True:
            for i in range(0, len(self.thrs)):
                await cc.go_to_thread(i)
                print('awake in', cc)
                await cc.sleep(0.5)

    @property
    def spawn(self):
        return self.get_random_queue().spawn

    @property
    def sleep(self):
        return self.get_random_queue().sleep

    @property
    def offload(self):
        return self.get_random_queue().offload

    def get_random_queue(self):
        return random.choice(self.thrs)
