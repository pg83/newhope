def gen_unpack_node(pkg):
    mpkg = y.mgr_pkg_mark(pkg)
    vis_name = pkg[4:]

    return {
        'inputs': [y.build_scripts_path(), pkg],
        'output': mpkg,
        'build': [
            '. "$2" && source unpackage $(basename "$3")'
        ],
    }


def print_v3_node(n):
    yield n['output'] + ': ' + ' '.join(n['inputs'])

    for l in n['build']:
        yield '\t' + l


def print_v3_node_2(n):
    yield n['output']

    yield ': '

    for i in n['inputs']:
        yield i
        yield ' '

    yield '\n'

    for l in n['build']:
        yield '\t'
        yield l
        yield '\n'


def do_apply_node(root, by_name):
    node = root['node']
    nnn = node['name']
    cc = node.get('host', {})
    pp = y.gen_pkg_path(root)

    def iter_groups():
        yield 'all'

        cur = ''

        for x in (nnn, y.small_repr(cc)):
            cur += '-'
            cur += x

            yield cur[1:]

    for name in iter_groups():
        name = name.replace('_', '-')

        if name in by_name:
            by_name[name].append(pp)
        else:
            by_name[name] = [pp]


def iter_nodes(nodes):
    vn = y.visit_nodes
    rn = y.restore_node

    for n in vn(nodes):
        yield rn(n), n


def gen_unpack_node_for_node(r):
    return y.gen_unpack_node(y.gen_pkg_path(r))


def preprocess(cmd, r):
    yield from cmd
    yield gen_unpack_node_for_node(r)


def reducer(v, by_deps):
    return v

    if len(v) < 2:
        return v

    v = list(sorted(set(v)))
    k = 'r' + y.struct_dump_bytes(v)

    s = by_deps.get(k, {})

    if s:
        s['c'] = s['c'] + 1
    else:
        by_deps[k] = {'c': 1, 'v': v}

    return [k]


def replacer(data):
    def func(s):
        return s.replace('-v4', '-v5' + data[4:7])

    return func


async def build_makefile(nodes, internal=False):
    by_noid = {}

    def iter1():
        for r, n in iter_nodes(nodes):
            by_noid[y.calc_noid_base(r)] = r

            yield r

    def iter2():
        trash = {
            'replacer': lambda x: x,
            'restore_node': lambda x: by_noid[y.calc_noid_base(y.restore_node(x))],
            'extra': 1,
            'reducer': lambda x: x,
        }

        for r in list(iter1()):
            r['trash'] = trash

            yield r

    def iter3():
        for r in list(iter2()):
            yield r, y.struct_dump_bytes(y.print_one_node(r))

    def iter4():
        by_deps = {}
        my_reducer = lambda v: reducer(v, by_deps)

        for r, data in list(iter3()):
            trash = {
                'replacer': replacer(data),
                'restore_node': lambda x: by_noid[y.calc_noid_base(y.restore_node(x))],
                'extra': 3,
                'reducer': my_reducer,
            }

            r['trash'] = trash

            yield r

    def iter5_0():
        by_name = {}

        yield y.build_scripts_run()

        for x in y.iter_workspace():
            yield x

        for r in list(iter4()):
            res = y.print_one_node(r)
            do_apply_node(r, by_name)

            for l in preprocess(res, r):
                yield l

        for name in sorted(by_name.keys()):
            yield {
                'output': name,
                'inputs': sorted(frozenset(by_name[name])),
                'build': [],
            }

    def iter5():
        by_out = {}

        for l in iter5_0():
            k = l['output']
            id = y.burn(l)

            if k in by_out:
                assert by_out[k] == id
            else:
                by_out[k] = id

                yield l

    if internal:
        def iter6():
            for cmd in iter5():
                yield {
                    'deps2': cmd['inputs'],
                    'deps1': [cmd['output']],
                    'cmd': cmd['build'],
                }

        mk = y.MakeFile()
        mk.init_from_parsed({'lst': list(iter6()), 'flags': {}})

        return y.dumps_mk(mk)

    def iter6():
        for cmd in iter5():
            for l in print_v3_node_2(cmd):
                yield l

            if cmd['build']:
                yield '\n\n'

    res = ''

    for v in iter6():
        res += v

    return res
