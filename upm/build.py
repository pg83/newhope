import os


def print_v3_node(n):
    def iter_lines():
        yield n['output'] + ': ' + ' '.join(n['inputs'])

        for l in n['build']:
            yield '\t' + l

    return '\n'.join(iter_lines()) + '\n\n'


def do_apply_node(root, by_name):
    node = root['node']()
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


def preprocess(cmd):
    yield cmd


def build_makefile(nodes, verbose):
    def iter1():
        by_id = {}

        def gen_iter(r):
            def dep_iter():
                for n in r['ptrs']():
                    yield by_id[n]

            return dep_iter

        for r, n in iter_nodes(nodes):
            by_id[n] = r
            r['deps'] = gen_iter(r)

            yield r

    def iter2():
        for r in list(iter1()):
            r['noid2'] = y.calc_noid([y.print_one_node(r, lambda x: x), r['noid']])

            yield r

    def iter3():
        for r in list(iter2()):
            r['noid'] = r.pop('noid2')

            yield r

    def iter4():
        by_name = {}
        by_deps = {}

        def reducer(v):
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

        def do():
            yield y.build_scripts_run()

            for r in list(iter3()):
                res = y.print_one_node(r, reducer)
                do_apply_node(r, by_name)

                for l in preprocess(res):
                    yield l

                yield y.gen_unpack_node(y.gen_pkg_path(r))

        for n in do():
            yield print_v3_node(n)

        for k in sorted(by_deps.keys()):
            yield k + ': ' + ' '.join(by_deps[k]['v'])

        for name in sorted(by_name.keys()):
            res = name + ': ' + ' '.join(sorted(set(by_name[name])))

            if len(res) < 500:
                yield res

    return '\n'.join(iter4()) + '\n'

