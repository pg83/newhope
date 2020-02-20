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


def gen_unpack_node_for_node(r):
    return y.gen_unpack_node(y.gen_pkg_path(r))


def preprocess(cmd, r):
    yield from cmd
    yield gen_unpack_node_for_node(r)


def build_makefile(nodes, kind):
    def iter3(nodes):
        for n in y.visit_nodes(nodes):
            yield y.restore_node(n)

    if kind == 'json':
        return y.json.dumps(list(iter3(nodes)), indent=4, sort_keys=True)

    def iter4():
        by_name = {}

        yield y.build_scripts_run()

        for x in y.iter_workspace():
            yield x

        for r in list(iter3(nodes)):
            res = y.print_one_node(r)
            do_apply_node(r, by_name)

            for l in preprocess(res, r):
                yield l

        for name in sorted(by_name.keys()):
            yield {
                'output': name,
                'inputs': y.uniq_list_x(by_name[name]),
                'build': [],
            }

    def iter5():
        by_out = {}

        for l in iter4():
            k = l['output']
            id = y.burn(l)

            if k in by_out:
                assert by_out[k] == id
            else:
                by_out[k] = id

                yield l

    if kind in ('internal', 'data'):
        def iter6():
            for cmd in iter5():
                yield {
                    'deps2': cmd['inputs'],
                    'deps1': [cmd['output']],
                    'cmd': cmd['build'],
                }

        if kind == 'data':
            return list(iter6())
        elif kind == 'internal':
            mk = y.MakeFile()

            mk.init_from_parsed({'lst': list(iter6()), 'flags': {}})

            return mk
        else:
            assert False

    assert kind == 'text'

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
