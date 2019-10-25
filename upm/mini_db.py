import hashlib
import traceback

from marshal import loads, dumps
#from json import loads, dumps

from upm_iface import y


def deep_copy(x):
    return loads(dumps(x))


def struct_dump_bytes(p):
    return struct_dump_bytes_ex(p)[0]


def struct_dump_bytes_ex(p):
    try:
        data = dumps(p)

        return hashlib.md5(data).hexdigest()[:16], data
    except Exception as e:
        y.xprint(e, p, color='yellow')

        raise e


# intern_struct vs. deref_pointer

III = {}
VVV = []


def struct_ptr_ex(s):
    k, v = struct_dump_bytes_ex(s)

    return 's:' + k, v


def struct_ptr(s):
    return struct_ptr_ex(s)[0]


def key_struct_ptr_ex(n):
    k, v = struct_ptr_ex(n)

    return 'k:' + k[2:12], v


def key_struct_ptr(n):
    return key_struct_ptr_ex(n)[0]


def intern_list(l):
    assert None not in l
    return intern_data({'l': l})


def load_list(ptr):
    return load_data(ptr)['l']


def intern_struct(s):
    return intern_data({'s': s})


def load_struct(ptr):
    return load_data(ptr)['s']


def check_db():
    for k, v in III.iteritems():
        assert k == VVV[v][1]

    for n, k in VVV:
        assert key_struct_ptr(n) == k or key_struct_ptr([n[0], {}]) == k
        assert VVV[III[k]][1] == k

    return 'db ok, ncount = ' + str(len(III)) + ', size = ' + str(len(dumps_db([III, VVV])))


def intern_data(n):
    k = key_struct_ptr(n)

    if k in III:
        p = III[k]

        assert VVV[p][1] == k
    else:
        VVV.append((n, k))
        p = len(VVV) - 1
        III[k] = p

    return pointer(p)


def load_data(ptr):
    return deref_pointer(ptr)


def pointer(p):
    return mangle_pointer(p)


def hash_key(p):
    return VVV[demangle_pointer(p)][1]


def mangle_pointer(p):
    return 'p:' + str(p)


def demangle_pointer(p):
    assert p[0] == 'p'
    return int(p[2:])


def deref_pointer_x(v):
    return VVV[demangle_pointer(v)]


def deref_pointer(v):
    return deref_pointer_x(v)[0]


def is_pointer(x):
    if str(x)[:2] == 'p:':
        try:
            return demangle_pointer(x)
        except TypeError:
            pass

    return False
