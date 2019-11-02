
import os


def print_v3_node(n):
    def iter_lines():
        yield n['output'] + ': ' + ' '.join(n['inputs'])

        for l in n['build']:
            yield '\t' + l

    return '\n'.join(iter_lines()) + '\n\n'


def do_apply_node(root, by_name):
    node = root['node']
    nnn = node['name']
    cc = node.get('constraint', {})
    pp = y.gen_pkg_path(root)

    def iter_groups():
        yield 'all'
        yield nnn
        x = nnn + '-' + y.short_const_1(cc.get('host', {}))
        yield x
        yield x + y.short_const_1(cc.get('target', {}))

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
    yield cmd
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
        return 'v5' + data[:4] + s[4:]

    return func


def build_makefile(nodes, verbose):
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
        }

        for r in list(iter1()):
            r['trash'] = trash

            yield r

    def iter3():
        for r in list(iter2()):
            yield r, y.struct_dump_bytes(y.print_one_node(r, lambda x: x))

    def iter4():
        for r, data in list(iter3()):
            trash = {
                'replacer': replacer(data),
                'restore_node': lambda x: by_noid[y.calc_noid_base(y.restore_node(x))],
                'extra': 3,
            }

            r['trash'] = trash

            yield r

    def iter5():
        by_name = {}
        by_deps = {}
        my_reducer = lambda v: reducer(v, by_deps)

        def do():
            yield y.build_scripts_run()

            for r in list(iter4()):
                res = y.print_one_node(r, my_reducer)
                do_apply_node(r, by_name)

                for l in preprocess(res, r):
                    yield l

        for n in do():
            yield print_v3_node(n)

        for k in sorted(by_deps.keys()):
            yield k + ': ' + ' '.join(by_deps[k]['v'])

        for name in sorted(by_name.keys()):
            res = name + ': ' + ' '.join(sorted(set(by_name[name])))

            if len(res) < 500:
                yield res

    return '\n'.join(iter5()) + '\n'

