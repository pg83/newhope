import hashlib
import json

from marshal import loads, dumps


isf = y.inspect.iscoroutinefunction


def make_name(f, n):
    f.__name__ = n

    return f


def uniq_list_3(l):
    return list(sorted(frozenset(l)))


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


def uniq_list_x(iter):
    return list(uniq_list_0(iter))


def to_lines(text):
    def iter_l():
        for l in text.split('\n'):
            l = l.strip()

            if l:
                yield l

    return list(iter_l())


def dc(x):
    try:
        return loads(dumps(x))
    except Exception as e:
        if 'unmarshal' in str(e):
            return y.copy.deepcopy(x)

        raise e


class IncCounter(object):
    def __init__(self):
        self.c = 0
        self.l = y.threading.Lock()

    def __iter__(self):
        while True:
            with self.l:
                begin = self.c
                end = begin + 10000
                self.c = end

            for i in range(begin, end):
                yield i

    def inc_counter(self):
        it = iter(self)

        def func():
            return next(it)

        func()

        return func


@y.singleton
def inc_counter_holder():
    return IncCounter()


def inc_counter():
    return inc_counter_holder().inc_counter()


def modify_list(k, d, f):
    d[k] = f(d.get(k, []))


def append_list(k, d, v):
    modify_list(k, d, lambda l: l + [v])


def prepend_list(k, d, v):
    modify_list(k, d, lambda l: [v] + l)


def ensure_value(k, d, v):
    if k not in d:
        d[k] = v

    return d[k]


def jd(d):
    return y.json.dumps(d, indent=4, sort_keys=True)
