import sys
import json
import time
import binascii
import random

from upm_iface import y


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


@y.cached()
def gen_fetch_node(url):
    res = {
        'node': {
            'kind': 'fetch',
            'name': 'fetch_url',
            'url': url,
            'pkg_full_name': y.calc_pkg_full_name(url),
            'build': [
                'cd $(INSTALL_DIR) && ((wget -O $(URL_BASE) $(URL) >& $(INSTALL_DIR/log/wget.log)) || (curl -L -k -o $(URL_BASE) $(URL) >&$(INSTALL_DIR/log/curl.log)) && ls -la',
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
