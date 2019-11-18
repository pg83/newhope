import hashlib
import json

from marshal import loads, dumps


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
