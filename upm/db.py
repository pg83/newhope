import sys
import json
import time
import binascii
import random

from upm_iface import y
from upm_ft import struct_dump_bytes, dumps as dumps_db, cached, singleton
from upm_gen_id import calc_pkg_full_name
from upm_helpers import xprint

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
        assert key_struct_ptr(n) == k
        assert VVV[III[k]][1] == k

    return 'db ok, ncount = ' + str(len(III)) + ', size = ' + str(len(dumps_db([III, VVV])))


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
        for z in do(x):
            yield z


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


def restore_node(ptr, rd=True):
    res = deref_pointer(ptr)

    if rd:
        f = restore_node
    else:
        f = lambda x: x

    def iter_deps():
        for p in deref_pointer(res[1]):
            yield f(p)

    def get_node():
        return deref_pointer(res[0])

    return {
        'node': get_node,
        'deps': iter_deps,
        'noid': binascii.hexlify(VVV[demangle_pointer(ptr)][1]),
    }


def restore_node_simple(v):
    v = restore_node(v, rd=False)

    return {
        'node': v['node'](),
        'deps': list(v['deps']()),
        'noid': v['noid'],
    }


def store_node_impl(node, extra_deps):
    def iter_deps():
        for x in node['deps']:
            assert x
            yield x

        for x in extra_deps:
            assert x
            yield x

    node = y.fix_v2(node)

    return intern_struct([
        intern_struct(node['node']),
        intern_list(list(iter_deps())),
    ])


def store_node_plain(node):
    return store_node_impl(node, [])


def store_node(node):
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


def debug_print(y):
    def iter_node(x):
        n = x['node']()
        nn = n['name'] + ':'

        yield nn + 'node:', n

        deps = list(x['deps']())

        yield nn + 'deps:', deps

        for d in deps:
            nd = nn + 'dep:'

            yield nd, d

            try:
                for a, b in iter_values(d):
                    yield nd + a, b
            except Exception as e:
                yield nd + a + ':error', str(e)

    def iter_values(x):
        yield 'val:' + 'x', x

        try:
            for a, b in iter_node(restore_node(x)):
                yield 'val:' + a, b
        except Exception as e:
            yield 'val:' + 'error', str(e)

        try:
            yield 'val:' + 'deref_pointer', deref_pointer(x)
        except Exception as e:
            yield 'val:' + 'error', str(e)

    xprint('----------------------------\n' + '\n'.join(x + ' = ' + str(y) for x, y in iter_values(y)), color='yellow')

