import queue

LOOPS = []


@y.lookup
@y.cached()
def loop_by_name(name):
    if name.endswith('_LOOP'):
        y.debug('construct loop %s', name)
        
        return Loop(name[:-5])

    raise AttributeError()


def thread_id():
    return str(y.thread.get_ident())

            
#######################################


def broadcast_channel(name, hid=None):
    if not hid:
        hid = thread_id()
    
    def func(ev):
        for c in [x for x in LOOPS]:
            c.write_channel(name, hid)(ev)
            
    return func


def write_channel(loop_name, name, hid):
    return loop_by_name(loop_name).write_channel(name, hid)
    

def uniq_write_channel(loop_name, hid):
    return write_channel(loop_name, str(y.random.random()), hid)


def read_callback(loop_name, name):
    return loop_by_name(loop_name).read_callback(name)


def read_callback_from_channel(channel):
    return channel.read_callback()

###############################3        

@y.singleton
def debug_pubsub():
    return '/pubsub' in y.verbose


class AllDone(Exception):
    pass


def ep_key(cb, hid, name):
    return y.struct_dump_bytes([cb.__name__, hid, name])[:16]


def raise_done():
    raise AllDone()


class WriteChannel(object):
    def __init__(self, queue, hid):
        self.q = queue
        self.h = hid

    def __call__(self, ev):
        self.q.send_event(ev, self.h)

    def read_callback(self, same_hid=False):
        hid = self.h

        if not same_hid:
            hid = None
        
        return self.q.read_callback(hid)

    
class PSQueue(dict):
    def __init__(self, args):
        self.__dict__ = self
        self.update(args)

    def read_callback(self, hid):
        return self.loop.read_callback(self.name, hid=hid)
        
    def write_channel(self, hid):
        return WriteChannel(self, hid)

    def send_event(self, ev, hid):
        self.queue_event({'name': self.name, 'data': ev, 'hid': hid})

    def send_event_real(self, ev):
        self.prev.append(ev)
        subs = self.subs

        for k in sorted(subs.keys()):
            endpoint = subs[k]
            endpoint['cb'](endpoint, ev)

        self.loop.on_event(ev)
            
    def queue_event(self, ev):
        self.loop.send_event(lambda: self.send_event_real(ev))
        
    def subscribe_cb_raw(self, cb, hid):
        key = ep_key(cb, hid, self.name)
        subs = self.subs
            
        if key in subs:
            return subs[key]['wq']
        else:
            subs[key] = {'cb': cb, 'hid': hid, 'wq': self.write_channel(hid), 'name': self.name}

        endpoint = subs[key]

        for msg in self.prev:
            cb(endpoint, msg)
                
        return endpoint['wq']
    
    def real_cb(self, cb, endpoint, msg):
        try:
            if endpoint['hid'] != msg['hid']:
                res = msg['data']
                    
                try:
                    cb(res)
                except TypeError:
                    try:
                        cb(endpoint['wq'], res)
                    except TypeError:
                        cb(res)
        except AllDone:
            self.loop.del_pub_sub(endpoint['name'])
        except y.StopNow:
            self.loop.stop()
                    
    def subscribe_cb(self, cb, hid):
        f = lambda x, y: self.real_cb(cb, x, y)
        f.__name__ = 'wrap_realcb_' + str(cb.__module__) + '_' + str(cb.__name__)
    
        return self.subscribe_cb_raw(f, hid)


class Loop(dict):
    def __init__(self, name):
        self.__dict__ = self
        self.q = queue.SimpleQueue()
        self.n = name
        self.a = []

        LOOPS.append(self)
        self.read_all_events_cb(y.pubsub.on_ext_event)
            
    @property
    def thr_id(self):
        try:
            return self.t
        except AttributeError:
            return 'no id'

    def iter_queue(self):
        while True:
            while True:
                try:
                    yield self.q.get_nowait()
                except y.queue.Empty:
                    t = 0.01

            while True:
                try:
                    yield self.q.get(False, t)

                    break
                except y.queue.Empty:
                    t = min(t * 1.2 + 0.01, 0.2)
    
    def loop_base(self):
        for f in self.iter_queue():
            f()
            
    def run_loop(self, init=[]):
        self.t = thread_id()

        for f in init:
            self.q.put(f)
        
        try:
            try:
                return self.loop_base()
            except y.StopNow:
                pass
        finally:
            y.os.abort()
            self.pop('t')
    
    def stop(self):
        self.q.put(y.stop_iter)

    def send_event(self, func):
        if self.thr_id == thread_id():
            try:
                func()
            except y.StopNow:
                self.stop()
        else:
            self.q.put(func)

    @property
    @y.cached_method
    def channel(self):
        return self.write_channel('LOOP', 'common')
    
    def new_queue(self, name):
        return PSQueue({
            'name': name,
            'subs': {},
            'prev': [],
            'loop': self,
        })

    def del_pub_sub(self, name):
        def do():
            if name in self:
                ps = self.pop(name)
                ps.queue_event(raise_done)
                ps.pop('subs')

        self.send_event(do)

    def get_queue(self, name):
        if name not in self:
            self[name] = self.new_queue(name)

        return self[name]

    def write_channel(self, name, hid):
        return self.get_queue(name).write_channel(hid)
                
    def subscribe_cb(self, name, cb, hid):
        return self.get_queue(name).subscribe_cb(cb, hid)

    def read_callback(self, name, hid=None):
        def functor(func):
            self.subscribe_cb(name, func, hid or func.__name__)
            
            return func
    
        return functor

    def read_all_events_cb(self, func):
        self.a.append(func)

    def on_event(self, ev):
        if self.a:
            try:
                xev = {'tags': [self.n.upper(), ev['name'].upper(), ev['hid'].upper()], 'data': ev['data']}

                for f in self.a:
                    f(xev)
            except Exception:
                y.os.abort()
        
    def print_data(self):
        for k, v in  self.items():
            v = y.deep_copy(v)
            v['prev'] = len(v['prev'])
            y.xprint_w('k =', k, 'v =', v)


@y.defer_constructor
def init_pub_sub_shutdown():
    def registry():
        def stop_all_loops(arg):
            if arg['signal'] == 'INT':
                do_stop()

            if arg['signal'] == 'DOWN' and 'when' in arg:
                do_stop()

        @y.singleton
        def do_stop():
            for c in LOOPS:
                c.stop()

    registry()
