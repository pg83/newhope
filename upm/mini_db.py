import hashlib

from marshal import loads, dumps

from upm_iface import y


def deep_copy(x):
    return loads(dumps(x))


def struct_dump_bytes(p):
    try:
        return hashlib.md5(dumps(p)).hexdigest()[:16]
    except Exception as e:
        y.xprint(e, p, color='yellow')

        raise e


# intern_struct vs. deref_pointer

III = {}
VVV = []
ZZZ = {}


def struct_ptr(s):
    return struct_dump_bytes(s)


def key_struct_ptr(n):
    return struct_ptr(n)[:8]


def intern_list(l):
    assert None not in l
    return intern_struct(l)


def intern_struct(n):
    k = key_struct_ptr(n)

    if k in III:
        p = III[k]
    else:
        VVV.append((n, k))
        p = len(VVV) - 1
        III[k] = p

    return pointer(p)


def check_db():
    for k, v in III.iteritems():
        assert k == VVV[v][1]

    for n, k in VVV:
        assert key_struct_ptr(n) == k or key_struct_ptr([n[0], {}]) == k
        assert VVV[III[k]][1] == k

    return 'db ok, ncount = ' + str(len(III)) + ', size = ' + str(len(dumps_db([III, VVV])))


def pointer(p):
    return mangle_pointer(p)


def hash_key(p):
    return demangle_pointer(p)


def mangle_pointer(p):
    return p - 1


def demangle_pointer(p):
    return p + 1


def deref_pointer(v):
    return VVV[demangle_pointer(v)][0]

