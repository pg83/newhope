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


def struct_dump_bytes(p):
    return hashlib.md5(dumps(p)).hexdigest()[:16]


def struct_dump_bytes_json(p):
    return hashlib.md5(json.dumps(p, sort_keys=True)).hexdigest()
