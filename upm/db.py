import sys
import json
import time
import binascii
import random
import itertools

from upm_iface import y

hash_key = y.hash_key
deref_pointer = y.deref_pointer
load_struct = y.load_struct


def visit_nodes(nodes, debug=False):
    s = set()

    def check_hash(k):
        assert k

        kk = hash_key(k)

        if kk in s:
            return True

        s.add(kk)

        return False


    def do(k):
        if check_hash(k):
            return

        yield k

        for x in y.restore_node(k)['ptrs']():
            for v in list(do(x)):
                yield v

    for x in nodes:
        for z in do(x):
            yield z


def restore_node(ptr):
    res = y.load_list(ptr)
    deps = y.load_list(res[1])

    def iter_deps():
        for p in deps:
            yield restore_node(p)

    def iter_deps_ptr():
        return deps

    @y.singleton
    def get_node():
        return load_struct(res[0])

    def iter_keys():
        yield hash_key(ptr)

        for d in deps:
            yield hash_key(d)

    x = list(iter_keys())
    id = 'i:' + y.key_struct_ptr(x)[2:]

    return {
        'node': get_node,
        'deps': iter_deps,
        'ptrs': iter_deps_ptr,
        'noid': id,
    }


def restore_node_simple(v):
    u = hash_key(v)
    v = restore_node(v)

    return {
        'node': v['node'](),
        'deps': v['ptrs'](),
        'noid': v['noid'],
    }


def store_node_impl(node, extra_deps):
    node = y.fix_v2(node)

    return y.intern_list([
        y.intern_struct(node['node']),
        y.intern_list(list(itertools.chain(node['deps'], extra_deps))),
    ])


def store_node_plain(node):
    return store_node_impl(node, [])


def store_node(node):
    def extra():
        if 'url' in node['node']:
            yield y.gen_fetch_node(node['node']['url'])

    return store_node_impl(node, list(extra()))
