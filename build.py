import os
import json
import random
import subprocess
import fcntl
import sys
import shutil
import gen_id
import hashlib

from user import add_tool_deps, TOOLS, tools
from gen_id import struct_dump

import gen_id


def fix_fetch_url(src, depth):
    return 'tar --strip-components ' + str(depth) + ' -xf ' + '$(BUILD_DIR)/fetched_urls/' + os.path.basename(src) + ';'


def install_dir(pkg):
    return '$(PREFIX)/managed/' + gen_id.to_visible_name(pkg)


def bin_dir(pkg):
    return install_dir(pkg) + '/bin'


def lib_dir(pkg):
    return install_dir(pkg) + '/lib'


def inc_dir(pkg):
    return install_dir(pkg) + '/include'


def subst_values(data, pkg, deps):
    subst = [
        ('$(INSTALL_DIR)', '$(PREFIX)/private/$(VISIBLE)'),
        ('$(VISIBLE)', gen_id.to_visible_name(pkg)),
        ('$(BUILD_DIR)', '$(PREFIX)/workdir/' + gen_id.struct_dump(pkg)),
        ('$(PYTHON)', '/usr/bin/python'),
        ('$(PKG_FILE)', gen_pkg_path({'node': pkg})),
        ('\n\n', '\n'),
    ]

    if 'url' in pkg:
        src = pkg['url']

        src1 = [
            ('$(FETCH_URL)', fix_fetch_url(src, 1)),
            ('$(FETCH_URL_2)', fix_fetch_url(src, 2)),
            ('$(URL)', src),
            ('$(URL_BASE)', os.path.basename(src)),
        ]

        subst = subst + src1

    def iter_dirs():
        for x in deps:
            node = x['node']
            name = node['name']

            yield '$(' + name.upper() + '_BIN_DIR)', bin_dir(node)
            yield '$(' + name.upper() + '_LIB_DIR)', lib_dir(node)
            yield '$(' + name.upper() + '_INC_DIR)', inc_dir(node)

    for k, v in subst + list(iter_dirs()):
        data = data.replace(k, v)

    return data


def calc_mode(name):
    if '-gz-' in name[:15]:
        return 'z'

    if '-xz-' in name[:15]:
        return 'J'

    if '-tar-' in name[:15]:
        return ''

    raise Exception('shit happen')


def get_pkg_link(p):
    m = p.replace('/repo/', '/managed/')

    if not os.path.isdir(m):
        with open(p, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)

            try:
                if not os.path.isdir(m):
                    os.makedirs(m)
                    subprocess.check_output(['tar', '-x' + calc_mode(p[p.find('/repo/') + 6:]) + 'f', p], cwd=m, shell=False)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    return m


def prepare_pkg(fr, to):
    print >>sys.stderr, 'will package', fr, 'to package', to

    tmp = to + '_' + str(int(random.random() * 1000000))

    subprocess.check_output(['tar', '-c' + calc_mode(to[to.index('-') - 1:]) + 'f', tmp, '.'], cwd=fr, shell=False)
    os.rename(tmp, to)

    print >>sys.stderr, 'done packaging'

    return to


def gen_pkg_path(v):
    return '$(PREFIX)/repo/' + gen_id.to_visible_name(v['node'])


def gen_fetch_node(url):
    return {
        'node': {
            'kind': 'fetch',
            'name': 'fetch_url_node',
            'file': __file__,
            'url': url,
            'build': [
                '#pragma manual deps',
                'cd $(INSTALL_DIR) && ((wget -q $(URL) >& wget.log) || (curl -q -k -O $(URL) >& curl.log)) && ls -la',
            ],
            'prepare': [
                '#pragma manual deps',
                'mkdir -p $(BUILD_DIR)/fetched_urls/',
                'ln -s `pwd`/$(URL_BASE) $(BUILD_DIR)/fetched_urls/',
            ],
        },
        'deps': [],
    }


def build_makefile_impl(node, extra_nodes=[]):
    def fix_node(n):
        n = json.loads(json.dumps(n))
        data = '\n'.join(n['node']['build'] + n['node'].get('prepare', []))
        deps = [fix_node(x) for x in n['deps']]

        if '$(FETCH_URL' in data:
            n['deps'] = deps + [gen_fetch_node(n['node']['url'])]
        else:
            n['deps'] = deps

        return n

    def iter_all():
        yield fix_node(node)

        for x in extra_nodes:
            yield fix_node(x)

    s = dict()

    def visit(node):
        k = struct_dump(node)

        if k not in s:
            s[k] = node

            yield node

            for x in node['deps']:
                for k in visit(x):
                    yield k

    def iter_all_nodes():
        for v in iter_all():
            for n in visit(v):
                yield n

    full = list(iter_all_nodes())
    by_name = {}

    for n in full:
        k = struct_dump(n)
        n['id'] = k
        s[k] = n
        name = n['node']['name']

        if name in by_name:
            by_name[name].append(gen_pkg_path(n))
        else:
            by_name[name] = [gen_pkg_path(n)]

    def iter_nodes():
        for v in full:
            yield print_one_node(v)

    def iter_by_name():
        for name in sorted(by_name.keys()):
            yield name + ': ' + ' '.join(sorted(by_name[name]))

    return '\n\n'.join(iter_nodes()) + '\n' + 'all: ' + ' '.join([gen_pkg_path(v) for v in s.values()]) + '\n' + '\n'.join(iter_by_name())


def print_one_node(v):
    data = print_one_node_once(v, [])
    tools = add_tool_deps(v['node'], data)

    while True:
        new_data = print_one_node_once(v, tools)

        if new_data == data:
            return data

        data = new_data


def print_one_node_once(v, mined_tools):
    deps = v['deps'] + mined_tools

    def iter_part():
        target = gen_pkg_path(v)
        yield '## ' + struct_dump(v)
        yield  os.path.basename(target) + ' ' + target + ': all_struct ' + ' '.join(gen_pkg_path(x) for x in deps)

        def iter_body():
            yield 'mkdir -p $(INSTALL_DIR) $(BUILD_DIR)'

            for x in deps:
                yield '## prepare ' + x['node']['name']
                pkg_path = gen_pkg_path(x)

                yield '$(PYTHON) $(PREFIX)/runtime/entry.py -- get_pkg_link ' + pkg_path

                prepare = x['node'].get('prepare', [])

                if prepare:
                    yield 'cd ' + pkg_path.replace('/repo/', '/managed/')

                for p in prepare:
                    yield p


            yield '## prepare main dep'
            yield 'cd $(BUILD_DIR)'

            for x in v['node']['build']:
                yield x

            # yield 'ls -la $(INSTALL_DIR); ls -la $(BUILD_DIR); env;'
            yield '$(PYTHON) $(PREFIX)/runtime/entry.py -- prepare_pkg $(INSTALL_DIR) $(PKG_FILE)'
            #yield 'rm -rf $(BUILD_DIR) $(INSTALL_DIR)'

        for l in iter_body():
            yield '\t' + l

        yield '\n'

    def flt_part():
        for l in iter_part():
            ls = l.strip()

            if not ls:
                continue

            if ls.startswith('##'):
                yield l

            if ls.startswith('#'):
                continue

            yield l

    data = '\n'.join(flt_part()) + '\n'

    for i in (1, 2):
        data = subst_values(data, v['node'], deps)

    return data


def add_boilerplate():
    all_struct = """
        all_struct: $(PREFIX)/private $(PREFIX)/repo $(PREFIX)/managed $(PREFIX)/workdir

        $(PREFIX)/private:
                mkdir -p $(PREFIX)/private

        $(PREFIX)/repo:
                mkdir -p $(PREFIX)/repo

        $(PREFIX)/managed:
                mkdir -p $(PREFIX)/managed

        $(PREFIX)/workdir:
                mkdir -p $(PREFIX)/workdir
    """

    def iter_lines():
        for l in all_struct.split('\n'):
            if 'mkdir' in l:
                yield '\t' + l.strip()
            else:
                yield l.strip()

    return '\n'.join(iter_lines())


def build_makefile(n, prefix=''):
    all_tools = tools({'host': 'x86_64', 'target': 'x86_64'})

    return '.ONESHELL:\nSHELL=/bin/bash\n.SHELLFLAGS=-exc\n\n' + add_boilerplate().replace('$(PREFIX)', prefix) + '\n' + build_makefile_impl(n, extra_nodes=all_tools).replace('$(PREFIX)', prefix).replace('$', '$$')
