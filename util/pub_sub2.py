nt = y.collections.namedtuple
ic = y.inc_counter()


DEFUN = nt('DEFUN', ['f'])
SKIP = nt('SKIP', [])
DEACT = nt('DEACT', [])
STATEFUL = nt('STATEFUL', [])


@y.cached(key=lambda x: y.burn(x))
def list_to_set(lst):
    return frozenset(lst)


@y.singleton
def is_debug():
    if '/debug/pubsub' in y.verbose:
        return True

    return False


def guess_print_data(data):
    if data is None:
        return '[eof]'

    if data.__class__.__name__ == 'ROW':
        return str(data)

    try:
        if 'func' in data:
            return data['func']['gen'] + '-' + data['func']['base']

        if 'name' in data:
            return data['name']
    except TypeError:
        pass
    
    return str(data)


class ACCEPT(object):
    __slots__ = ('tags')

    def __init__(self, *tags):
        self.tags = frozenset(list_to_set(list(tags)))

    def __str__(self):
        return '(ACCEPT {' + ', '.join(sorted(self.tags)) + '})'

    def __repr__(self):
        return str(self)


class PROVIDES(ACCEPT):
    pass
    

class EOP(object):
    __slots__ = ('extra')

    def __init__(self, *extra):
        self.extra = list(extra)

    def iter_me(self):
        for x in self.extra:
            if cmd_name(x) == 'eop':
                for y in x.iter_me():
                    yield y
            else:
                yield x

    def __str__(self):
        return '(EOP (' + ', '.join([str(x) for x in self.iter_me()]) + '))'
                

class DATA(object):
    __slots__ = ('tags', 'data')

    def __init__(self, tags=[], data=None):
        self.tags = list_to_set(tags)
        self.data = data
        
    def __str__(self):
        return '(DATA {' + ', '.join(sorted(self.tags)) + '}, ' + guess_print_data(self.data) + ')'

    def __repr__(self):
        return str(self)


def ELEM(data):
    return DATA(tags=[], data=data)


def EOS():
    return ELEM(None)


def FIN():
    return y.EOP(y.EOS(), y.DEACT())


class ROW(object):
    __slots__ = ('producer', 'consumers', 'data', 'uid')
            
    def __init__(self, producer, data):
        self.producer = producer
        self.consumers = set([producer])
        self.data = data
        self.uid = ic()

    def __str__(self):
        return str({
            'producer': self.producer,
            'consumers': self.consumers,
            'data': self.data,
            'uid': self.uid,
        })

    
class FunBase(object):
    def __init__(self, f, parent, n):
        self.p = parent
        self.f = f
        self.accept = []
        self.inqueue = y.collections.deque()
        self.n = n
        self.active_x = True
        self.consumed_rows = 0

    @property
    def __name__(self):
        return self.f.__name__

    @property
    def name(self):
        return self.__name__
        
    @property
    def active(self):
        return self.active_x
        
    def new_accept(self, tags):
        is_debug() and y.debug('new accept', self.f.__name__, tags)
        
        if self.accept:
            self.accept.append(frozenset(self.accept.pop() | frozenset(tags)))
        else:
            self.accept.append(frozenset(tags))
            
    def deactivate(self):
        is_debug() and y.debug('deactivate', str(self))
        self.active_x = False

    @property
    def unconsumed_rows(self):
        return len(self.inqueue)
        
    def __str__(self):
        return str({
            'name': self.name,
            'accept': self.accept,
            'inqueue': len(self.inqueue),
            'n': self.n,
            'klass': self.__class__.__name__,
            'active': self.active,
            'consumed': self.consumed_rows,
            'unconsumed': self.unconsumed_rows,
        })
        
    @property
    def iface(self):
        return self.p
    
    def add_data(self, data):
        if not self.active:
            return
            
        for el in data:
            for x in self.add_el(el):
                yield x

    def add_el(self, el):
        if self.accept_data(el):
            el.consumers.add(self.n)
            self.inqueue.append(el)
            
            yield el.uid

    def check_1_in_2(self, a, b):
        for x in a:
            if x in b:
                return True

        return False
                
    def accept_data(self, el):
        if self.n in el.consumers:
            return False
        
        for a in self.accept:
            if self.check_1_in_2(el.data.tags, a):
                return True

        return False

    def iter_data_full(self):
        while len(self.inqueue):
            try:
                yield self.inqueue.popleft()
                self.consumed_rows += 1
            except IndexError:
                return
            
    def iter_data(self):
        for r in self.iter_data_full():
            yield r.data
            
    def step_1(self):
        is_debug() and y.debug('will call', str(self))

        if self.active:
            res = [ROW(self.n, d) for d in self.step_0()]

            is_debug() and y.debug('afteer call', str(self))
            
            return res
            
        return []

    def step(self):
        return self.step_1()

    
class Iterator(FunBase):
    def __init__(self, f, parent, n):
        FunBase.__init__(self, f, parent, n)
        self.iter = f(self)
        self.stateful = False
        self.provides = frozenset()
        
    def step_0(self):
        def iter_cmd(v):
            if cmd_name(v) == 'eop':
                for x in v.iter_me():
                    yield x

                yield EOP()
            else:
                yield v
                    
        def iter_0():
            if self.stateful and not self.inqueue:
                return
            
            for u in self.iter:
                for v in iter_cmd(u):
                    cm = cmd_name(v)

                    if cm == 'eop':
                        return
                    elif cm == 'stateful':
                        self.stateful = True
                    elif cm == 'provides':
                        self.provides = v.tags
                    elif cm == 'data':
                        if not v.tags:
                            v.tags = self.provides

                        yield v
                    else:
                        yield v

            if self.stateful:
                y.os.abort()
            
            self.iter = self.f(self)

        return iter_0()

            
class Scheduler(Iterator):
    def __init__(self, f, parent, n):
        Iterator.__init__(self, f, parent, n)
            
    async def step(self):
        is_debug() and y.debug('will call scheduler', str(self))
        
        if self.active:
            for x in [self.p.funcs[0]] + list(reversed(self.p.funcs)):
                self.inqueue.extend(x.step_1())

        return []

            
def kl_name(v):
    return v.__class__.__name__


def cmd_name(v):
    return kl_name(v).lower()


def all_timers():
    return (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 4.0, 8.0, 16.0)


def tout_to_teg(tout):
    return 'TIMER_' + str(int(10 * tout))

            
def timer(parent):
    timers = []

    yield EOP(ACCEPT())
    
    for t in all_timers():
        timers.append((t, y.time.time()))

    for t in all_timers():
        yield DATA(['ps:trash'], {'tag': tout_to_teg(t)})
        
    yield EOP()

    while True:
        yield SKIP()

        tags = []
        now = y.time.time()
    
        def iter_timers():
            for tout, begin in timers:
                if begin + tout < now:
                    tags.append(tout_to_teg(tout))
                    
                    yield tout, now
                else:
                    yield tout, begin

        timers = list(iter_timers())

        for tag in tags:
            yield DATA([tag], {'now': now})
        
        yield EOP()


def debugger(parent):
    yield EOP(ACCEPT())
    
    while True:
        for i in parent.iter_data():
            is_debug() and y.debug(str(i))
            
        yield EOP()


def tresher(iface):
    yield EOP(ACCEPT('ps:trash'))

    for data in iface.iter_data():
        data = data.data

        if 'tag' in data:
            yield ACCEPT(data['tag'])

    yield EOP()
        

class PubSubLoop(object):
    def __init__(self, ctl=None):
        self.ctl_ = ctl
        self.funcs = []
        self.by_name = set()
        self.ext = y.collections.deque()
        self.active_ns = set()

        self.add_fun(self.scheduler_step, Scheduler)
        self.add_fun(self.run_ext_queue)
        self.add_fun(self.unused_row)
        #self.add_fun(tresher)
        #self.add_fun(timer)
        
        if is_debug():
            self.add_fun(debugger)
            
        self.add_fun(self.state_checker)
        self.activate('ps')

    @property
    def ctl(self):
        return self.ctl_ or y.async_loop
        
    def activate(self, ns):
        self.active_ns.add(ns)

    def deactivate(self, ns):
        self.active_ns.remove(ns)
        
    def is_active_ns(self, ns):
        return ns in self.active_ns
        
    def run_ext_queue(self, iface):
        yield y.EOP(y.ACCEPT('ps:ext queue'))

        for i in iface.iter_data():
            while self.ext:
                ev = self.ext.pop()
                
                yield DATA(ev['tags'], ev['data'])
                
        yield y.EOP()
        
    def add_fun(self, ff, cls=Iterator):
        name = ff.__name__

        if name not in self.by_name:
            self.by_name.add(name)
            self.funcs.append(cls(ff, self, len(self.funcs)))

    def active(self):
        return any(x.active for x in self.funcs)

    def state_checker(self, iface):
        yield EOP(ACCEPT('ps:check state'))

        for row in iface.iter_data():
            if any(f.active for f in self.funcs[iface.n + 1:]):
                break

            for f in self.funcs[:iface.n + 1]:
                f.deactivate()

        yield EOP()

    def unused_row(self, iface):
        yield EOP(ACCEPT('ps:unused row'))

        unused = []
        
        for row in iface.iter_data():
            unused.append(row)

        if len(unused) > 100:
            for r in unused:
                yield r

            unused.clear()
            
        yield EOP()

    async def run(self, init=[]):
        for f in init:
            self.add_fun(f)
        
        async def pub_sub_cycle(ctl):
            while self.active():
                await self.step()

        return await self.ctl.spawn(pub_sub_cycle, 'pub_sub_cycle')

    def scheduler(self):
        return self.funcs[0]
            
    async def step(self):
        s = self.scheduler()
        
        await s.step()
        
    def scheduler_step(self, iface):
        extra = []
        
        def iter_0():
            if self.ext:
                yield ROW(0, DATA(['ps:ext queue'], {}))
                
            for row in list(iface.iter_data_full()):
                yield row
                    
                if row.uid % 100 == 0:
                    yield ROW(0, DATA(['ps:check state'], {}))

            for row in [x for x in extra]:
                yield row
        
        for row in iter_0():
            f = self.funcs[row.producer]
            c = row.data
            cn = cmd_name(c)

            if cn == 'deact':
                f.deactivate()
            elif cn == 'defun':
                self.add_fun(c.f)
            elif cn == 'accept':
                f.new_accept(list_to_set(c.tags))
            elif cn == 'data':
                used = False
                
                for f in self.funcs:
                    for uid in f.add_el(row):
                        is_debug() and y.debug(str(f), 'accept', str(row))
                        used = True

                if not used:
                    extra.append(ROW(0, DATA(['ps:unused row'], row)))
            elif cn == 'skip':
                pass
            else:
                y.critical('bad command', cn)
                y.os.abort()
                
        yield EOP()

    def on_ext_event(self, ev):
        self.ext.append(ev)
        
    def wrap(self, f):
        self.add_fun(f)

        return f

    def wrap_coro(self, c):
        def wrapper_in(iface):
            outqueue = y.collections.deque()
            
            async def wrapper(ctl):
                async def in_q():
                    while True:
                        try:
                            yield iface.inqueue.popleft()
                        except IndexError:
                            await ctl.sleep(0.01)
                
                async for x in c(ctl, in_q()):
                    outqueue.append(x)

            hndl = self.ctl.spawn(wrapper, 'pubsub_' + c.__name__)

            while True:
                try:
                    yield outqueue.popleft()
                except IndexError:
                    y.time.sleep(0.01)

        wrapper_in.__name__ = 'wrapper_' + c.__name__

        self.add_fun(wrapper_in)

        return c


pubsub = PubSubLoop()
