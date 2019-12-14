nt = y.collections.namedtuple
ic = y.inc_counter()


DEFUN = nt('DEFUN', ['f'])
DECORO = nt('DECORO', ['f'])
SKIP = nt('SKIP', [])
DEACT = nt('DEACT', [])
STATEFUL = nt('STATEFUL', [])


@y.cached(key=lambda x: y.burn(x))
def list_to_set(lst):
    return frozenset(lst)


@y.singleton
def is_debug():
    return 'debug' in y.config.get('pubsub', '')


def pretty_dumps(obj):
    cls = y.json.JSONEncoder
            
    def default(o):
        try:
            o.__json__
        except AttributeError:
            return str(o)
        
        return o.__json__()

    return cls(default=default, indent=4, sort_keys=True).encode(obj).replace('"', '').replace(',\n', '\n')


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


class PROVIDES(object):
    __slots__ = ('tags')

    def __init__(self, *tags):
        self.tags = frozenset(list_to_set(list(tags)))

    def __str__(self):
        return '(PROVIDES {' + ', '.join(sorted(self.tags)) + '})'

    def __repr__(self):
        return str(self)
    

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
        res = '(DATA {' + ', '.join(sorted(self.tags)) + '}, ' + guess_print_data(self.data) + ')'

        return res.replace('{', '(').replace('}', ')')

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
        self.consumers = {producer}
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
        self.produced = 0
        
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

        h1 = y.burn(self.accept)
        
        if self.accept:
            self.accept.append(frozenset(self.accept.pop() | frozenset(tags)))
        else:
            self.accept.append(frozenset(tags))

        h2 = y.burn(self.accept)

        return h1 != h2
            
    def deactivate(self):
        is_debug() and y.debug('deactivate', str(self))
        self.active_x = False

    @property
    def unconsumed_rows(self):
        return len(self.inqueue)
        
    def __str__(self):
        return str(self.__json__())
        
    def __repr__(self):
        return str(self)

    def __json__(self):
        def fmt_accept(a):
            if a:
                return list(a[0])

            return []
            
        return {
            'name': self.name,
            'accept': fmt_accept(self.accept),
            'inqueue': len(self.inqueue),
            'n': self.n,
            'klass': self.__class__.__name__,
            'active': self.active,
            'consumed': self.consumed_rows,
            'unconsumed': self.unconsumed_rows,
            'produced': self.produced,
        }
    
    @property
    def iface(self):
        return self.p
    
    def push(self, el):
        if self.accept_data(el):
            el.consumers.add(self.n)
            self.inqueue.append(el)
            
            return True

        return False
                
    def accept_data(self, el):
        if not self.active:
            return False
        
        if self.n in el.consumers:
            return False

        return True

    def iter_data_full(self):
        while True:
            try:
                yield self.inqueue.popleft()
                self.consumed_rows += 1
            except IndexError:
                return
            
    def iter_data(self):
        for r in self.iter_data_full():
            yield r.data
            
    def step_1(self):
        return list(self.step_01())

    def step_01(self):
        for d in self.step_0():
            yield ROW(self.n, d)
            
    def step(self):
        return self.step_1()

    
class Iterator(FunBase):
    def __init__(self, f, parent, n):
        FunBase.__init__(self, f, parent, n)
        self.iter = f(self)
        self.stateful = False
        self.provides = frozenset()
        
    def step_0(self):
        if not self.active:
            return
        
        def iter_cmd(v):
            if cmd_name(v) == 'eop':
                for x in v.iter_me():
                    yield x

                yield EOP()
            else:
                yield v
                
        def iter_00():
            while True:
                if self.stateful and not self.inqueue:
                    return
                    
                for u in self.iter:
                    yield u

                if self.stateful:
                    y.os.abort()

                is_debug() and y.debug('rebuild iter for ', self.name)
            
                self.iter = self.f(self)
                    
        def iter_0():
            for u in iter_00():
                for v in iter_cmd(u):
                    cm = cmd_name(v)
                    
                    if cm == 'eop':
                        return
                    elif cm == 'stateful':
                        self.stateful = True
                    elif cm == 'provides':
                        self.provides = v.tags
                    elif cm == 'data':
                        self.produced += 1
                        
                        if not v.tags:
                            v.tags = self.provides

                        yield v
                    else:
                        yield v

        yield from iter_0()

            
class Scheduler(Iterator):
    def __init__(self, f, parent, n):
        Iterator.__init__(self, f, parent, n)
            
    async def step(self):
        is_debug() and y.debug('will call scheduler', str(self))
        
        if self.active:
            s = self.p.funcs[0]
            
            for x in self.p.funcs[1:]:
                if x.active:
                    self.inqueue.extend(s.step_1())
                    self.inqueue.extend(x.step_01())

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
        self.net = {}
        self.by_name = set()
        self.ext = y.collections.deque()
        self.active_ns = set()

        self.add_fun(self.scheduler_step, Scheduler)
        self.add_fun(self.run_ext_queue)
        self.add_fun(self.unused_row)
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
                
                yield y.EOP(DATA(ev['tags'], ev['data']))

        
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

            for f in self.funcs:
                f.deactivate()

        yield EOP()

    def unused_row(self, iface):
        yield EOP(ACCEPT('ps:unused row'))

        while True:
            for row in iface.iter_data():
                yield row.data.data

            yield EOP()

    async def run(self, init=[], coro=[]):
        for f in init:
            self.add_fun(f)

        for c in coro:
            self.wrap_coro(c)
        
        async def pub_sub_cycle(ctl):
            while self.active():
                await self.step()

        return await self.ctl.spawn(pub_sub_cycle, 'pub_sub_cycle')

    def scheduler(self):
        return self.funcs[0]
            
    async def step(self):
        s = self.scheduler()
        
        await s.step()

    def rebuild_net(self):
        net = y.collections.defaultdict(list)

        for f in self.funcs:
            for a in f.accept:
                for el in a:
                    net[el].append(f)

        #is_debug() and y.debug('rebuild net', pretty_dumps(net))

        self.net = net
        
    def scheduler_step(self, iface):
        is_debug() and y.debug('scheduler step in')
        
        extra = []
        
        def iter_0():
            if self.ext:
                yield ROW(0, DATA(['ps:ext queue'], {}))
                
            if y.random.random() < 0.1:
                yield ROW(0, DATA(['ps:check state'], {}))
                
            for row in list(iface.iter_data_full()):
                yield row
                    
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
            elif cn == 'decoro':
                self.wrap_coro(c.f)
            elif cn == 'accept':
                if f.new_accept(list_to_set(c.tags)):
                    self.rebuild_net()
            elif cn == 'data':
                is_debug() and y.debug('new data', c)
                
                used = False

                for tag in row.data.tags:
                    for f in self.net.get(tag, []):
                        if f.push(row):
                            is_debug() and y.debug(f.name, 'accept', row)
                            
                            used = True

                if not used:
                    extra.append(ROW(0, DATA(['ps:unused row'], row)))
            elif cn == 'skip':
                pass
            else:
                y.critical('bad command', cn)
                y.os.abort()

        is_debug() and y.debug('scheduler step out')
        
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
                async for x in c(ctl, y.deque_iter_async(iface.inqueue, sleep=ctl.sleep)):
                    outqueue.append(x)

            hndl = self.ctl.spawn(wrapper, 'async_' + c.__name__)

            while True:
                try:
                    yield outqueue.popleft()
                except IndexError:
                    yield EOP()

        self.add_fun(y.set_name(wrapper_in, 'sync_' + c.__name__))

        return c
