import sys
import json
import time
import binascii
import random

from .ft import struct_dump_bytes, dumps as dumps_db, cached, singleton
from .gen_id import calc_pkg_full_name


III = {}
VVV = []
ZZZ = {}


def struct_ptr(s):
    return struct_dump_bytes(s)


def intern_list(l):
    assert None not in l
    return intern_struct(l)


def intern_struct(n):
    k = struct_ptr(n)[:8]

    if k in III:
        p = III[k]
    else:
        VVV.append((n, k))
        p = len(VVV) - 1
        III[k] = p

    return pointer(p)


def check_db():
    t1 = time.time()

    for k, v in III.iteritems():
        assert k == VVV[v][1]

    t2 = time.time()

    return 'db ok, ncount = ' + str(len(III)) + ', size = ' + str(len(dumps_db([III, VVV]))) + ', check time = ' + str(t2 - t1) + 's'


def visit_nodes(nodes):
    s = set()

    def do(k):
        kk = hash_key(k)

        if kk not in s:
            s.add(kk)

            yield k

            def iter_node_links():
                node = deref_pointer(k)

                for x in deref_pointer(node[1]):
                    yield x

                for x in deref_pointer(node[0]).get('extra_nodes', []):
                    yield x

            for x in iter_node_links():
                for v in do(x):
                    yield v

    for x in nodes:
        for y in do(x):
            yield y


def pointer(p):
    return mangle_pointer(p)


def hash_key(p):
    return demangle_pointer(p)


def mangle_pointer(p):
    return p


def demangle_pointer(p):
    return p


def deref_pointer(v):
    return VVV[demangle_pointer(v)][0]


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
        'noid': binascii.hexlify(VVV[demangle_pointer(ptr)][1]),
    }


def store_node_impl(node, extra_deps):
    if node is None:
        raise Exception('shit')

    def iter_deps():
        for x in node['deps']:
            if x:
                yield x

        for x in extra_deps:
            if x:
                yield x

    return intern_struct([
        intern_struct(node['node']),
        intern_list(list(iter_deps())),
    ])


def store_node_plain(node):
    return store_node_impl(node, [])


def store_node(node):
    if node is None:
        raise Exception('shit')

    def extra():
        if 'url' in node['node']:
            yield gen_fetch_node(node['node']['url'])

    return store_node_impl(node, list(extra()))


@cached()
def gen_fetch_node(url):
    res = {
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
    }

    return store_node_plain(res)
