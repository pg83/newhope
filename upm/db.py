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

        for x in y.restore_node_deps(k):
            for v in do(x):
                yield v

    for x in nodes:
        for z in do(x):
            yield z


@y.cached()
def restore_node(ptr):
    res = y.load_list(ptr)

    v = {
        'node': y.load_struct(res[0]),
        'deps': y.load_list(res[1]),
    }

    v['noid'] = y.calc_noid_base(v)

    return v


def restore_node_node(ptr):
    return y.load_struct(y.load_list(ptr)[0])


def restore_node_deps(ptr):
    return y.load_list(y.load_list(ptr)[1])


def store_node_impl(node, extra_deps):
    return y.intern_list([
        y.intern_struct(node['node']),
        y.intern_list(list(y.itertools.chain(node['deps'], extra_deps))),
    ])


def store_node_plain(node):
    return store_node_impl(node, [])


def store_node(node):
    def extra():
        if 'node' in node and 'url' in node['node'] and node.get('do_fetch_node', True):
            yield y.gen_fetch_node(node['node']['url'])

    return store_node_impl(node, list(extra()))
