import json
import time
import binascii

from .ft import struct_dump_bytes, dumps as dumps_db, cached
from .gen_id import calc_pkg_full_name


III = {}


def struct_ptr(s):
    return struct_dump_bytes(s)


def intern_struct(n):
    k = struct_ptr(n)
    III[k] = n

    return pointer(k)


def check_db():
    t1 = time.time()

    for k, v in III.iteritems():
        assert k == struct_ptr(v)

    t2 = time.time()

    return 'db ok, ncount = ' + str(len(III)) + ', size = ' + str(len(dumps_db(III))) + ', check time = ' + str(t2 - t1) + 's'


def visit_node(root):
    s = set()

    def do(k):
        kk = k

        if kk not in s:
            s.add(kk)

            yield k

            for x in deref_pointer(deref_pointer(k)[1]):
                for v in do(x):
                    yield v

    for x in do(root):
        yield x


def pointer(p):
    return mangle_pointer(p)


def mangle_pointer(p):
    return (p, 'p')


def demangle_pointer(p):
    assert p[1] == 'p'

    return p[0]


def deref_pointer(v):
    return III[demangle_pointer(v)]


def restore_node(ptr):
    res = deref_pointer(ptr)

    def iter_deps():
        for p in deref_pointer(res[1]):
            yield restore_node(p)

    def get_node():
        return deref_pointer(res[0])

    return {
        'node': get_node,
        'deps': iter_deps,
        'noid': binascii.hexlify(demangle_pointer(ptr)),
    }


def store_node_impl(node, extra_deps):
    def iter_deps():
        for x in node['deps']:
            yield x

        for x in extra_deps:
            yield x

    return intern_struct([intern_struct(node['node']), intern_struct(list(iter_deps()))])


def store_node_plain(node):
    return store_node_impl(node, [])


def store_node(node):
    def extra():
        if 'url' in node['node']:
            yield gen_fetch_node(node['node']['url'])

    return store_node_impl(node, list(extra()))


@cached
def gen_fetch_node(url):
    return store_node_plain({
        'node': {
            'kind': 'fetch',
            'name': 'fetch_url',
            'file': __file__,
            'url': url,
            'pkg_full_name': calc_pkg_full_name(url),
            'build': [
                'cd $(INSTALL_DIR) && ((wget -O $(URL_BASE) $(URL) >& wget.log) || (curl -L -k -o $(URL_BASE) $(URL) >& curl.log)) && ls -la',
            ],
            'prepare': [
                'mkdir -p $(BUILD_DIR)/fetched_urls/',
                'ln $(CUR_DIR)/$(URL_BASE) $(BUILD_DIR)/fetched_urls/',
            ],
            'codec': 'tr',
        },
        'deps': [],
    })
