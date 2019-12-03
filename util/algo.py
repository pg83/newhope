import hashlib
import json

from marshal import loads, dumps


isf = y.inspect.iscoroutinefunction


def uniq_list_2(iter, key):
    visited = set()

    for x in iter:
        p = key(x)

        if p not in visited:
            visited.add(p)

            yield (p, x)


def uniq_list_1(iter, key):
    for p, x in uniq_list_2(iter, key):
        yield x


def uniq_list_0(iter):
    return uniq_list_1(iter, lambda x: x)


def to_lines(text):
    def iter_l():
        for l in text.split('\n'):
            l = l.strip()

            if l:
                yield l

    return list(iter_l())


def burn(p):
    return struct_dump_bytes(p)


def struct_dump_bytes(p):
    return hashlib.md5(dumps(p)).hexdigest()[:16]


def struct_dump_bytes_json(p):
    return hashlib.md5(json.dumps(p, sort_keys=True)).hexdigest()


def deep_copy(x):
    try:
        return loads(dumps(x))
    except Exception as e:
        if 'unmarshal' in str(e):
            return y.copy.deepcopy(x)

        raise e


def inc_counter():
    c = [int(y.random.random() * 10000)]

    def func():
        c[0] += 1
        return c[0]

    return func


def compile_func(template, _async, name, mod_name):
    replaces = {
        True: {'[async]': 'async', '[await]': 'await', 'kind': 'async', '[sleep]': 'y.async_loop.sleep'},
        False: {'[async] ': '', '[await] ': '', 'kind': 'sync', '[sleep]': 'y.time.sleep'},        
    }

    def subst(t):
        for k, v in replaces[_async].items():
            t = t.replace(k, v)

        return t
    
    template = subst(template)
    name = subst(name)
    mod_name = subst(mod_name)
    code = compile(template, mod_name.replace('.', '/') + '.py', 'exec')
    mod = __yexec__(template, module_name=mod_name)

    return mod[name]


def template_engine(func):
    def gen(_async):
        subst = {
            True: 'async',
            False: 'sync',
        }
        
        tmpl = func()
        mod_name = func.__module__ + '.' + subst[_async]
        name = func.__name__

        return compile_func(tmpl, _async, name, mod_name)

    select = {
        True: gen(True),
        False: gen(False),
    }

    def wrapper(_async=False):
        return select[_async]

    wrapper.__name__ = func.__name__

    return wrapper


class TOut(object):
    def __init__(self):
        self.tout = 0

    def ok(self):
        self.tout = 0

    def bad(self):
        self.tout = min(self.tout * 1.1 + 0.001, 0.02)

    def current(self):
        if self.tout < 0.01:
            return 0

        return self.tout


@template_engine
def deque_iter():
    return """
[async] def deque_iter(q, sleep=None):
    sleep = sleep or [sleep]
    tout = y.TOut()

    [async] def xsleep(v):
        if v > 0:
            [await] sleep(v)
    
    while True:
        try:
            yield q.popleft()
            tout.ok()
        except IndexError:
            [await] xsleep(tout.current())
            tout.bad()
"""


deque_iter_sync = deque_iter(_async=False)
deque_iter_async = deque_iter(_async=True)
