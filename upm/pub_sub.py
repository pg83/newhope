@y.singleton
def all_pub_sub():
    return {}


class AllDone(Exception):
    pass


def raise_done():
    raise AllDone()


def new_pub_sub(name):
    res = {
        'name': name,
        'subs': [],
        'prev': y.collections.deque(),
    }

    all_pub_sub()[name] = res

    return res


def del_pub_sub(name):
    d = all_pub_sub()

    if name in d:
        ps = d.pop(name)
        queue_event(ps, raise_done)
        ps.pop('subs')
    

def real_cb(cb, endpoint, msg):
    try:
        msg = msg()
        
        if endpoint['hid'] != msg['hid']:
            res = msg['data']()
            
            try:
                res['hid'] = msg['hid']
            except TypeError:
                pass

            cb(res)
    except AllDone as e:
        del_pub_sub(endpoint['name'])


def subscribe_cb(name, cb, hid):
    return subscribe_cb_raw(name, lambda x, y: real_cb(cb, x, y), hid)


def subscribe_cb_raw(name, cb, hid):
    ps = get_queue(name)
    endpoint = {'cb': cb, 'hid': hid, 'wq': write_channel(name, hid), 'name': name}

    for msg in ps['prev']:
        cb(endpoint, msg)

    if 'subs' in ps:
        ps['subs'].append(endpoint)

        return endpoint['wq']


def subscribe_queue(name, hid):
    lst = y.collections.deque()

    def cb(endpoint, msg):
        real_cb(lst.append, endpoint, msg)

    wq = subscribe_cb_raw(name, cb, hid)

    def rq():
        while lst:
            yield lst.pop()

    return rq, wq


def get_queue(name):
    name + '1'

    d = all_pub_sub()

    if name not in d:
        res = new_pub_sub(name)
    else:
        res = d[name]
        
    return res


def send_event(queue, ev, hid):
    send_event_base(queue, lambda: ev, hid)


def send_event_base(queue, fev, hid):
    send_int_event(queue, lambda: {'name': queue['name'], 'data': fev, 'hid': hid})


def send_int_event(queue, fev):
    queue_event(queue, fev)


def queue_event(res, fev):
    res['prev'].append(fev)

    for endpoint in res['subs']:
        endpoint['cb'](endpoint, fev)
        

def write_channel(name, hid):
    res = lambda ev: send_event(res.__queue__, ev, res.__hid__)

    res.__name__ = name
    res.__hid__ = hid
    res.__queue__ = get_queue(name)
    
    return res


def read_from_write(channel):
    return subscribe_queue(channel.__name__, channel.__hid__)


def read_callback(name, hid):
    def functor(func):
        subscribe_cb(name, func, hid)

        return func

    return functor
