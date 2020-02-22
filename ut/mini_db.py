X = {}


def deep_copy_json(x):
    return y.json.loads(y.json.dumps(x))


def struct_ptr(s):
    return 's:' + y.burn(s)


def key_struct_ptr(n):
    return struct_ptr(n)[2:12]


def store_kv(k, v):
    X[k] = v


def load_kv(k):
    return X[k]


def intern_list(l):
    assert None not in l

    res1 = intern_struct({'l': l})
    res2 = 'l:' + y.burn(sorted(l))[:8]

    store_kv(res2, res1)

    return res2


def load_list(ptr):
    return load_struct(load_kv(ptr))['l']


def intern_struct(s):
    return intern_data({'s': s})


def load_struct(ptr):
    return load_data(ptr)['s']


def func_dumps(data):
    return y.marshal.dumps(data)


def func_loads(data):
    return y.marshal.loads(data)


def intern_data(n):
    n = func_dumps(n)
    k = y.hashlib.md5(n).hexdigest()[:12]

    store_kv(k, n)

    return pointer(k)


def load_data(k):
    return func_loads(load_kv(demangle_pointer(k)))


def pointer(p):
    return mangle_pointer(p)


def mangle_pointer(p):
    return 'p:' + p


def demangle_pointer(p):
    return p[2:]


def deref_pointer(p):
    return load_data(p)


def is_pointer(x):
    if str(x)[:2] == 'p:':
        try:
            return demangle_pointer(x)
        except TypeError:
            pass


def hash_key(p):
    return demangle_pointer(p)[:6]
