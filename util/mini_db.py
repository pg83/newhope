from marshal import loads, dumps


def deep_copy_json(x):
    return y.json.loads(y.json.dumps(x))


def struct_ptr(s):
    return 's:' + y.struct_dump_bytes(s)


def key_struct_ptr(n):
    return struct_ptr(n)[2:12]


def intern_list(l):
    assert None not in l
    return intern_struct({'l': l})


def load_list(ptr):
    return load_struct(ptr)['l']


def intern_struct(s):
    return intern_data({'s': s})
        

def load_struct(ptr):
    return load_data(ptr)['s']


# intern_struct vs. deref_pointer


class A(object):
    def __init__(self):
        self.III = {}
        self.VVV = []

    def intern_data(self, n):
        k = key_struct_ptr(n)

        if k in self.III:
            p = self.III[k]

            assert self.VVV[p][1] == k
        else:
            self.VVV.append((n, k))
            p = len(self.VVV) - 1
            self.III[k] = p

        return self.pointer(p)

    def load_data(self, ptr):
        return self.deref_pointer(ptr)

    def pointer(self, p):
        return self.mangle_pointer(p)

    def hash_key(self, p):
        return self.VVV[self.demangle_pointer(p)][1]

    def mangle_pointer(self, p):
        return 'p:' + str(p)

    def demangle_pointer(self, p):
        assert p[0] == 'p'
        return int(p[2:])

    def deref_pointer(self, v):
        return self.VVV[self.demangle_pointer(v)][0]

    def is_pointer(self, x):
        if str(x)[:2] == 'p:':
            try:
                return self.demangle_pointer(x)
            except TypeError:
                pass

    def check_db(self):
        for k, v in self.III.iteritems():
            assert k == self.VVV[v][1]
            assert k == key_struct_ptr(self.VVV[v][0])

        return 'db ok, ncount = ' + str(len(self.III))


class B(object):
    def __init__(self):
        self._v = {}

    def func1(self, data):
        return dumps(data)

    def func2(self, data):
        return loads(data)

    def intern_data(self, n):
        n = self.func1(n)
        k = y.hashlib.md5(n).hexdigest()[:12]
        self._v[k] = n
        return self.pointer(k)

    def load_data(self, k):
        return self.func2(self._v[self.demangle_pointer(k)])

    def pointer(self, p):
        return self.mangle_pointer(p)

    def mangle_pointer(self, p):
        return 'p:' + p

    def demangle_pointer(self, p):
        return p[2:]

    def defer_pointer(self, p):
        return self.load_data(p)

    def is_pointer(self, x):
        if str(x)[:2] == 'p:':
            try:
                return self.demangle_pointer(x)
            except TypeError:
                pass

    def hash_key(self, p):
        return self.demangle_pointer(p)[:6]

    def check_db(self):
        for k, v in self._v.iteritems():
            assert k == y.hashlib.md5(v).hexdigest()[:12]

        return 'all ok, count = ' + str(len(self._v))


@y.defer_constructor
def init():
    if '/adb' in y.verbose:
        v = A()
    else:
        v = B()

    for i in dir(v):
        if not i.startswith('__'):
            globals()[i] = eval('v.' + i)
            
    if '/check_db' in y.verbose:
        y.atexit.register(v.check_db)
