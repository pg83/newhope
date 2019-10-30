import os
import json
import random
import subprocess
import sys
import shutil
import hashlib
import itertools


def install_dir(pkg):
    return '$(WDP)/' + y.to_visible_name(pkg)


def bin_dir(pkg):
    return install_dir(pkg) + '/bin'


def lib_dir(pkg):
    return install_dir(pkg) + '/lib'


def inc_dir(pkg):
    return install_dir(pkg) + '/include'


@y.cached(key=lambda x: x['noid'])
def get_subst_values(x):
    def mn(x):
        return '$(WDM)' + x[6:]

    n = x['node']()['name'].upper().replace('-', '_')

    return [
        ('$(MNGR_' + n + '_DIR)', mn(install_dir(x))),
        ('$(MNGR_' + n + '_BIN_DIR)', mn(bin_dir(x))),
        ('$(MNGR_' + n + '_LIB_DIR)', mn(lib_dir(x))),
        ('$(MNGR_' + n + '_INC_DIR)', mn(inc_dir(x))),
    ]


@y.cached(key=lambda x: x['noid'])
def get_subst_values_3(root):
    def do():
        for x in itertools.chain([root], root['deps']()):
            for y in get_subst_values(x):
                yield y

    return list(do())


def subst_values(data, root):
    root_node = root['node']()

    def iter1():
        pkg_root = gen_pkg_path(root)

        yield ('$(INSTALL_DIR)', '$(WDP)/' + pkg_root[7:])
        yield ('$(BUILD_DIR)', '$(WDW)/' + root['noid'][2:])
        yield ('$(PYTHON)', '/usr/bin/python')
        yield ('$(PKG_FILE)', pkg_root)

    def iter2():
        if 'url' in root_node or 'pkg_full_name' in root_node:
            path = '$(MNGR_FETCH_URL_DIR)/' + root_node['pkg_full_name']
            mode = y.calc_mode(root_node['pkg_full_name'])
            tmpl = 'source untar_{ext} "{path}" {level}'

            yield ('$(FETCH_URL)', tmpl.format(ext=mode, path=path, level=1))
            yield ('$(FETCH_URL_2)', tmpl.format(ext=mode, path=path, level=2))
            yield ('$(FETCH_URL_FILE)', 'ln $(MNGR_FETCH_URL_DIR)/$(URL_BASE) $(URL_BASE)')

            if 'url' in root_node:
                yield ('$(URL)', root_node['url'])

            yield ('$(URL_BASE)', root_node['pkg_full_name'])

    return y.subst_kv_base(data, iter1(), iter2(), get_subst_values_3(root))


def mgr_pkg(x):
    return x.replace('$(WDR)', '$(WDM)') + '/done_mark'


def gen_pkg_path(v):
    return '$(WDR)/' + y.to_visible_name(v)


def do_apply_node(root, by_name):
    node = root['node']()
    nnn = node['name']
    cc = node.get('constraint', {})

    def iter_groups():
        yield 'all'
        yield nnn
        x = nnn + '-' + y.short_const_1(cc.get('host', {}))
        yield x
        yield x + y.short_const_1(cc.get('target', {}))

    for name in iter_groups():
        name = name.replace('_', '-')
        pp = gen_pkg_path(root)

        if name in by_name:
            by_name[name].append(pp)
        else:
            by_name[name] = [pp]


def iter_nodes(nodes):
    for n in y.visit_nodes(nodes):
        yield y.restore_node(n), n


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
            r['noid2'] = y.calc_noid([print_one_node(r, lambda x: x), r['noid']])

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

        for r in list(iter3()):
            res = print_one_node(r, reducer)
            do_apply_node(r, by_name)

            yield res
            yield print_internal_node(y.gen_unpack_node(gen_pkg_path(r)))

        for k in sorted(by_deps.keys()):
            yield k + ': ' + ' '.join(by_deps[k]['v'])

        for name in sorted(by_name.keys()):
            res = name + ': ' + ' '.join(sorted(set(by_name[name])))

            if len(res) < 500:
                yield res

    return '\n'.join(iter4()) + '\n'


def uniq_deps(d):
    return y.uniq_list_2(d, gen_pkg_path)


def rmmkcd(q, suffix=''):
    return 'rm -rf {q} || true; mkdir -p {q}{s}; cd {q}{s}'.format(q=q, s=suffix)


def prepare_prologue():
    yield 'set_path $(MNGR_BUILD_SCRIPTS_RUN_BIN_DIR):/bin:/usr/bin:/usr/local/bin'
    yield 'source prepare_env "$(INSTALL_DIR)" "$(BUILD_DIR)" "$(PKG_FILE)"'
    yield 'source header'


@y.singleton
def node_prologue():
    return list(prepare_prologue())


def print_internal_node(n):
    d = os.path.dirname(n['output'])

    def iter_lines():
        yield n['output'] + ': ' + ', '.join(n['inputs'])

        for l in n['build']:
            yield '\t' + l

    return '\n'.join(iter_lines()) + '\n\n'


def print_one_node(root, reducer):
    root_node = root['node']()

    target = gen_pkg_path(root)
    nodes = list(uniq_deps(root['deps']()))
    naked = root_node.get('naked', False)

    def iter_part1():
        yield target + ': ' + ' '.join(reducer([mgr_pkg(x[0]) for x in nodes])) + ' ## node ' + root['noid']

        if not naked:
            for l in node_prologue():
                yield l

        for pkg_path, x in nodes:
            pdir = pkg_path.replace('$(WDR)', '$(WDM)')

            for p in x['node']().get('prepare', []):
                yield p.replace('$(ADD_PATH)', 'add_path $(CUR_DIR)/bin').replace('$(CUR_DIR)', pdir)

        bld = root_node['build']

        if bld:
            if not naked:
                yield 'cd $BD'

            for x in bld:
                yield x

        if not naked:
            yield 'source footer {codec}'.format(codec=root_node['codec'])

    def iter_part2():
        def get_path(x):
            return x[8:].strip()

        lines1 = []
        paths = []
        lines2 = []

        for l in iter_part1():
            ll = l.strip()

            if ll.startswith('set_path') or ll.startswith('add_path'):
                paths.append(ll)
            else:
                if paths:
                    lines2.append(l)
                else:
                    lines1.append(l)

        for l in lines1:
            yield l

        yield 'export PATH=' + ':'.join([get_path(x) for x in reversed(paths)])

        for l in lines2:
            yield l

    def iter_lines():
        it = iter_part2()

        for l in it:
            yield l

            for x in it:
                yield '\t' + x

        yield ''
        yield ''

    data = '\n'.join(iter_lines())
    data = subst_values(data, root)

    return data
