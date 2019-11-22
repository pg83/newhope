LOOPS = []


@y.lookup
@y.cached()
def loop_by_name(name):
    if name.endswith('_LOOP'):
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


@y.singleton
def get_signal_channel():
    return y.MAIN_LOOP.write_channel('SIGNAL', 'common')


@y.singleton
def get_main_channel():
    return y.MAIN_LOOP.write_channel('MAIN', 'common')


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
        self.send_event_base(lambda: ev, hid)

    def send_event_base(self, fev, hid):
        self.queue_event(lambda: {'name': self.name, 'data': fev, 'hid': hid})

    def send_event_real(self, fev):
        #y.stderr.out('zzz', self.name, fev, self.prev)
        
        self.prev.append(fev)
        subs = self.subs

        try:
            for k in sorted(subs.keys()):
                endpoint = subs[k]
                endpoint['cb'](endpoint, fev)
        except StopIteration:
            pass
        
    def queue_event(self, fev):
        self.loop.send_event(lambda: self.send_event_real(fev))
        
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
        

class Loop(dict):
    def __init__(self, name):
        self.__dict__ = self
        self.q = y.Queue.Queue()
        self.n = name

        LOOPS.append(self)
            
    @property
    def thr_id(self):
        try:
            return self.t
        except AttributeError:
            return 'no id'
            
    def run_loop(self, init=lambda: []):
        self.t = thread_id()
        self.q.put(init)
        
        @self.channel.read_callback()
        def loop_cb(arg):
            y.stderr.out(self.n, 'loop arg', arg)
            self.q.put(lambda: arg)

        try:
            while True:
                res = self.q.get()()
                y.stderr.out('XXX', self.n, res)
        except StopIteration:
            y.stderr.out(self.n, 'exit now')
            
            return
        except:
            y.stderr.out(y.traceback.format_exc())
            y.os.abort()

    def stop(self):
        self.q.put(y.stop_iter)
            
    def send_event(self, func):
        if self.thr_id == thread_id():
            func()
        else:
            y.stderr.out('put', func, self.n)
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

    def subscribe_cb_raw(self, name, cb, hid):
        return self.get_queue(name).subscribe_cb_raw(cb, hid)
        
    def real_cb(self, cb, endpoint, msg):
        try:
            msg = msg()
        
            if endpoint['hid'] != msg['hid']:
                res = msg['data']()

                if debug_pubsub():
                    y.stderr.out('YYYY', res, endpoint)
                    
                try:
                    cb(res)
                except TypeError:
                    cb(endpoint['wq'], res)                    
        except AllDone as e:
            self.del_pub_sub(endpoint['name'])
        
    def print_data(self):
        for k, v in  self.items():
            v = y.deep_copy(v)
            v['prev'] = len(v['prev'])
            y.xprint_w('k =', k, 'v =', v)

    def subscribe_cb(self, name, cb, hid):
        f = lambda x, y: self.real_cb(cb, x, y)
        f.__name__ = 'wrap_realcb_' + str(cb.__module__) + '_' + str(cb.__name__)
    
        return self.subscribe_cb_raw(name, f, hid)

    def subscribe_queue(self, name, hid):
        lst = y.Queue.Queue()
        
        def cb(endpoint, msg):
            self.real_cb(lst.put, endpoint, msg)

        wq = self.subscribe_cb_raw(name, cb, hid)

        def rq():
            while True:
                yield lst.get()

        return rq, wq

    def read_callback(self, name, hid=None):
        def functor(func):
            self.subscribe_cb(name, func, hid or func.__name__)
            
            return func
    
        return functor
    

@y.defer_constructor
def init_pub_sub_shutdown():
    def registry():
        @y.abort_on_error
        @y.signal_channel.read_callback()
        def stop_all_loops(arg):
            if arg['signal'] == 'INT':
                do_stop()

            if arg['signal'] == 'DOWN' and 'when' in arg:
                do_stop()

        @y.singleton
        def do_stop():
            for c in LOOPS:
                c.stop()

    y.main_channel({'func': registry})
