import os
import json
import random
import subprocess
import fcntl
import sys
import shutil
import hashlib

from .user import add_tool_deps
from .db import visit_node, restore_node
from .gen_id import to_visible_name, short_const
from .ft import deep_copy, struct_dump
from .subst import subst_kv_base


def fix_fetch_url(src, depth):
    return 'tar --strip-components ' + str(depth) + ' -xf ' + '$(BUILD_DIR)/fetched_urls/' + os.path.basename(src)


def mv_file(src):
    name = os.path.basename(src)

    return 'cp $(BUILD_DIR)/fetched_urls/' + name + ' ' + name


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


def subst_values(data, root):
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
            src = root_node['url']

            yield ('$(FETCH_URL)', fix_fetch_url(src, 1))
            yield ('$(FETCH_URL_2)', fix_fetch_url(src, 2))
            yield ('$(FETCH_URL_FILE)', mv_file(src))
            yield ('$(URL)', src)
            yield ('$(URL_BASE)', os.path.basename(src))

    def iter3():
        for x in root['deps']():
            name = x['node']()['name'].upper()

            yield ('$(' + name + '_DIR)', install_dir(x))
            yield ('$(' + name + '_BIN_DIR)', bin_dir(x))
            yield ('$(' + name + '_LIB_DIR)', lib_dir(x))
            yield ('$(' + name + '_INC_DIR)', inc_dir(x))

    return subst_kv_base(data, iter1(), iter2(), iter3())


def calc_mode(name):
    if '-gz-' in name[:15]:
        return 'z'

    if '-xz-' in name[:15]:
        return 'J'

    if '-tr-' in name[:15]:
        return ''

    raise Exception('shit happen')


def get_pkg_link(p):
    m = p.replace('$(WDR)', '$(WDM)')

    if not os.path.isdir(m):
        with open(p, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)

            try:
                if not os.path.isdir(m):
                    os.makedirs(m)
                    subprocess.check_output(['tar', '-x' + calc_mode(p[p.find('$(WDR)') + 6:]) + 'f', p], cwd=m, shell=False)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    return m


def prepare_pkg(fr, to):
    tmp = to + '_' + str(int(random.random() * 1000000))

    try:
        os.makedirs(os.path.dirname(tmp))
    except OSError:
        pass

    subprocess.check_output(['tar', '-v', '-c' + calc_mode(to[to.index('-') - 1:]) + 'f', tmp, '.'], cwd=fr, shell=False)
    os.rename(tmp, to)

    return to


def gen_pkg_path(v):
    return '$(WDR)/' + to_visible_name(v)


def build_makefile_impl(node, replaces):
    full = list(visit_node(node))
    by_name = {}

    for ptr in full:
        root = restore_node(ptr)
        node = root['node']()
        nnn = node['name']

        for name in ('all', nnn, nnn + '-' + short_const(node.get('constraint', {}))):
            if name in by_name:
                by_name[name].append(gen_pkg_path(root))
            else:
                by_name[name] = [gen_pkg_path(root)]

    def iter_nodes():
        for ptr in full:
            yield print_one_node(restore_node(ptr), replaces)

    def iter_by_name():
        for name in sorted(by_name.keys()):
            yield name + ': ' + ' '.join(sorted(by_name[name]))

    def iter_parts():
        for n in iter_nodes():
            yield n

        for n in iter_by_name():
            yield n

    return '\n'.join(iter_parts()) + '\n'


def print_one_node(root, replaces):
    mined_deps = []
    root_deps = root['deps']

    def iter_root_deps():
        for x in root_deps():
            yield x

        for x in mined_deps:
            yield x

    root['deps'] = iter_root_deps
    data = print_one_node_once(root)

    while True:
        new_data = print_one_node_once(root)

        if new_data == data:
            pkg_id = os.path.basename(gen_pkg_path(root))
            real_id = hashlib.md5(data).hexdigest()[:4] + '-' +  pkg_id[4:]
            replaces[pkg_id] = real_id

            return data

        data = new_data


def print_one_node_once(root):
    iter_deps = root['deps']

    def iter_part():
        target = gen_pkg_path(root)

        yield '## ' + root['noid']
        yield os.path.basename(target) + ' ' + target + ': ' + ' '.join(gen_pkg_path(x) for x in iter_deps())

        def iter_body():
            yield '$(RM_TMP) $(INSTALL_DIR) $(BUILD_DIR)) || true'
            yield 'mkdir -p $(INSTALL_DIR) $(BUILD_DIR)'

            for x in iter_deps():
                xnode = x['node']()
                pkg_path = gen_pkg_path(x)

                yield '## prepare ' + xnode['name']
                yield '$(UPM) subcommand -- get_pkg_link ' + pkg_path

                prepare = xnode.get('prepare', [])

                if prepare:
                    pdir = pkg_path.replace('$(WDR)', '$(WDM)')

                    yield 'cd ' + pdir

                    for p in prepare:
                        yield p.replace('$(CUR_DIR)', pdir)

            bld = root['node']()['build']

            if bld:
                yield '## prepare main dep'
                yield 'cd $(BUILD_DIR)'

                for x in bld:
                    yield x

            yield '$(UPM) subcommand -- prepare_pkg $(INSTALL_DIR) $(PKG_FILE)'
            yield '$(RM_TMP) $(INSTALL_DIR) $(BUILD_DIR)'

        for l in iter_body():
            yield '\t' + l

        yield '\n'

    def flt_part():
        for l in iter_part():
            ls = l.strip()

            if not ls:
                continue

            if ls.startswith('##'):
                yield ls

            if ls.startswith('#'):
                continue

            yield l

    data = '\n'.join(flt_part()) + '\n'

    for i in (1, 2):
        data = subst_values(data, root)

    return data


def build_makefile(n):
    replaces = {}
    data = '.ONESHELL:\nSHELL=/bin/bash\n.SHELLFLAGS=-exc\n\n' + build_makefile_impl(n, replaces)

    for k, v in replaces.items():
        data = data.replace(k, v)

    return data
