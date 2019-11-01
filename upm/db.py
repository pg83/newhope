import sys
import json
import time
import binascii
import random
import itertools


def visit_nodes(nodes, debug=False):
    s = set()

    def check_hash(k):
        assert k

        kk = y.hash_key(k)

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


def calc_noid(v):
    return 'i:' + y.key_struct_ptr(v)[2:]


def restore_node(ptr):
    res = y.load_list(ptr)
    deps = y.load_list(res[1])

    def iter_deps_ptr():
        return deps

    @y.singleton
    def get_node():
        return y.load_struct(res[0])

    def iter_keys():
        yield y.hash_key(res[0])

        for d in deps:
            yield y.hash_key(d)

    return {
        'node': get_node,
        'ptrs': iter_deps_ptr,
        'noid': calc_noid(list(iter_keys())),
    }


def restore_node_simple(v):
    v = restore_node(v)

    return {
        'node': v['node'](),
        'deps': v['ptrs'](),
        'noid': v['noid'],
    }


def store_node_impl(node, extra_deps):
    return y.intern_list([
        y.intern_struct(node['node']),
        y.intern_list(list(itertools.chain(node['deps'], extra_deps))),
    ])


def store_node_plain(node):
    return store_node_impl(node, [])


def store_node(node):
    def extra():
        if 'node' in node and 'url' in node['node'] and node.get('do_fetch_node', True):
            yield y.gen_fetch_node(node['node']['url'])

    return store_node_impl(node, list(extra()))
