import os
import json
import random
import subprocess
import fcntl
import sys
import shutil
import hashlib

from .db import visit_nodes, restore_node, check_db, store_node
from .gen_id import to_visible_name, short_const_1
from .ft import deep_copy, singleton
from .subst import subst_kv_base
from .helpers import xprint


codecs = {
    'gz': 'z',
    'xz': 'J',
    'tr': '',
}


def install_dir(pkg):
    try:
        pkg['idir']
    except KeyError:
        pkg['idir'] = '$(WDP)/' + to_visible_name(pkg)

    return pkg['idir']


def bin_dir(pkg):
    return install_dir(pkg) + '/bin'


def lib_dir(pkg):
    return install_dir(pkg) + '/lib'


def inc_dir(pkg):
    return install_dir(pkg) + '/include'


def subst_values(data, root, iter_deps):
    def iter1():
        pkg_root = gen_pkg_path(root)

        yield ('$(INSTALL_DIR)', '$(WDP)/$(VISIBLE)')
        yield ('$(VISIBLE)', os.path.basename(pkg_root))
        yield ('$(BUILD_DIR)', '$(WDW)/' + root['noid'])
        yield ('$(PYTHON)', '/usr/bin/python')
        yield ('$(PKG_FILE)', pkg_root)
        yield ('\n\n', '\n')

    def iter2():
        root_node = root['node']()

        if 'url' in root_node:
            cmd = 'tar --strip-components %s -xf $(BUILD_DIR)/fetched_urls/$(URL_BASE)'

            yield ('$(FETCH_URL)', cmd % '1')
            yield ('$(FETCH_URL_2)', cmd % '2')
            yield ('$(FETCH_URL_FILE)', 'ln $(BUILD_DIR)/fetched_urls/$(URL_BASE) $(URL_BASE)')
            yield ('$(URL)', root_node['url'])
            yield ('$(URL_BASE)', root_node['pkg_full_name'])

    def iter3():
        def mn(x):
            return '$(WDM)' + x[6:]

        for x in iter_deps():
            for n in (x['node']()['name'], x['node']().get('func_name', '')):
                if n:
                    n = n.upper().replace('-', '_')

                    yield ('$(MNGR_' + n + '_DIR)', mn(install_dir(x)))
                    yield ('$(MNGR_' + n + '_BIN_DIR)', mn(bin_dir(x)))
                    yield ('$(MNGR_' + n + '_LIB_DIR)', mn(lib_dir(x)))
                    yield ('$(MNGR_' + n + '_INC_DIR)', mn(inc_dir(x)))

    return subst_kv_base(data, iter1(), iter2(), iter3())


def calc_mode(name):
    if '-tr-' in name:
        return ''

    if '-gz-' in name:
        return 'z'

    if '-xz-' in name:
        return 'J'

    raise Exception('shit happen')


def get_pkg_link(p, m):
    if not os.path.isdir(m):
        with open(p, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)

            try:
                if not os.path.isdir(m):
                    os.makedirs(m)
                    subprocess.check_output(['tar', '-x' + calc_mode(os.path.basename(p)) + 'f', p], cwd=m, shell=False)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    return m


def prepare_pkg(fr, to, codec):
    return [
        'mkdir -p $(WDR) ## archive package',
        'cd ' + fr + ' && ' + 'tar -v -c' + codecs[codec]  + 'f ' + to + '-tmp' + ' .',
        'mv ' + to + '-tmp ' + to,
    ]


def gen_pkg_path(v):
    return '$(WDR)/' + to_visible_name(v)


def build_makefile_impl(nodes, replaces):
    full = list(visit_nodes(nodes))
    by_name = {}

    for ptr in full:
        root = restore_node(ptr)
        node = root['node']()
        nnn = node['name']
        cc = node.get('constraint', {})

        def iter_groups():
            yield 'all'
            yield nnn
            x = nnn + '-' + short_const_1(cc.get('host', {}))
            yield x
            yield x + short_const_1(cc.get('target', {}))

        for name in iter_groups():
            name = name.replace('_', '-')

            if name in by_name:
                by_name[name].append(gen_pkg_path(root))
            else:
                by_name[name] = [gen_pkg_path(root)]

    def iter_nodes():
        for ptr in full:
            root = restore_node(ptr)
            data = print_one_node(root)
            link = to_visible_name(root)
            replaces[link] = hashlib.md5(data).hexdigest()[:8] + link[8:]

            yield data

    def iter_by_name():
        for name in sorted(by_name.keys()):
            yield name + ': ' + ' '.join(sorted(set(by_name[name])))

    def iter_parts():
        yield '## generated by ' + os.path.abspath(__file__)
        yield '.ONESHELL:'
        yield 'SHELL=/bin/sh'
        yield '\n\n'

        for n in iter_nodes():
            yield n

        for n in iter_by_name():
            yield n

    return '\n'.join(iter_parts()) + '\n'


def print_one_node(root):
    root_node = root['node']()
    old_root_deps = root['deps']

    def iter_deps():
        for x in old_root_deps():
            yield x

            for y in x['node']().get('extra_deps', []):
                yield restore_node(y)

    del root['deps']

    def iter_part():
        target = gen_pkg_path(root)

        def iter_nodes():
            visited = set()

            for x in iter_deps():
                p = gen_pkg_path(x)

                if p not in visited:
                    visited.add(p)

                    yield (p, x)

        nodes = list(iter_nodes())

        yield target + ': ' + ' '.join([x[0] for x in nodes])+ ' ## node ' + root['noid']

        def iter_body():
            def iter_env():
                env = [
                    ('TMPDIR', '"$(BUILD_DIR)"'),
                    ('PATH', '"/bin:/usr/bin"'),
                    ('SHELL', '"/bin/sh"'),
                    ('LC_ALL', '"C"'),
                    ('LANG', '"C"'),
                    ('HOME', '"/"'),
                    ('PWD', '"/"'),
                ]

                for k, v in env:
                    yield 'export ' + k + '=' + v

            yield 'cd /; /usr/bin/env; ' + '; '.join(iter_env())
            yield '$(RM_TMP) $(INSTALL_DIR) $(BUILD_DIR) || true'
            yield 'mkdir -p $(INSTALL_DIR) $(BUILD_DIR)'

            for pkg_path, x in nodes:
                xnode = x['node']()
                pdir = pkg_path.replace('$(WDR)', '$(WDM)')

                yield '$(UPM) -v subcommand -- get_pkg_link ' + pkg_path + ' ' + pdir + ' ## ' + xnode['name']

                prepare = xnode.get('prepare', [])

                if prepare:
                    yield 'cd ' + pdir

                    for p in prepare:
                        yield p.replace('$(ADD_PATH)', 'export PATH=$(CUR_DIR)/bin:$PATH').replace('$(CUR_DIR)', pdir)

            bld = root_node['build']

            if bld:
                yield 'cd $(BUILD_DIR) ## prepare main dep'

                for x in bld:
                    yield x

            for l in prepare_pkg('$(INSTALL_DIR)', '$(PKG_FILE)', root_node['codec']):
                yield l

            yield '$(RM_TMP) $(INSTALL_DIR) $(BUILD_DIR) || true'

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

    data = '\n\n'.join(flt_part()) + '\n'

    for i in (1, 2):
        data = subst_values(data, root, iter_deps)

    return data


def build_makefile(nodes, verbose):
    try:
        replaces = {}
        data = build_makefile_impl(nodes, replaces)

        return subst_kv_base(data, replaces.iteritems())
    finally:
        if verbose:
            xprint(check_db())
