from .ft import struct_dump


III = {}


def intern_struct(n):
    k = bytes(struct_dump(n)[:16])
    III[k] = n

    return pointer(k)


def visit_node(root):
    s = set()

    def do(k):
        kk = struct_dump(k)

        if kk not in s:
            s.add(kk)

            yield k

            for x in deref_pointer(deref_pointer(k)['d']):
                for v in do(x):
                    yield v

    for x in do(root):
        yield x


def pointer(p):
    return mangle_pointer(p)


def mangle_pointer(p):
    return (p,)


def demangle_pointer(p):
    return p[0]


def deref_pointer(v):
    return III[demangle_pointer(v)]


def restore_node(ptr):
    res = deref_pointer(ptr)

    def iter_deps():
        for p in deref_pointer(res['d']):
            yield restore_node(p)

    def get_node():
        return deref_pointer(res['n'])

    return {
        'node': get_node,
        'deps': iter_deps,
        'noid': demangle_pointer(ptr),
    }


def store_node_impl(node, extra_deps):
    def iter_deps():
        for x in node['deps']:
            yield x

        for x in extra_deps:
            yield x

    return intern_struct({
        'n': intern_struct(node['node']),
        'd': intern_struct(list(iter_deps())),
    })


def store_node_plain(node):
    return store_node_impl(node, [])


def store_node(node):
    def extra():
        if 'url' in node['node']:
            yield store_node_plain(gen_fetch_node(node['node']['url']))

    return store_node_impl(node, list(extra()))


def gen_fetch_node(url):
    return {
        'node': {
            'kind': 'fetch',
            'name': 'fetch_url',
            'file': __file__,
            'url': url,
            'build': [
                'cd $(INSTALL_DIR) && ((wget $(URL) >& wget.log) || (curl -k -O $(URL) >& curl.log)) && ls -la',
            ],
            'prepare': [
                'mkdir -p $(BUILD_DIR)/fetched_urls/',
                'ln -s $(CUR_DIR)/$(URL_BASE) $(BUILD_DIR)/fetched_urls/',
            ],
            'codec': 'tr',
        },
        'deps': [],
    }
