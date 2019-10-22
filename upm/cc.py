import sys
import subprocess
import platform
import os


from upm_iface import y
from upm_ft import deep_copy, cached, singleton
from upm_db import store_node, restore_node, deref_pointer, intern_struct
from upm_xpath import xp
from upm_helpers import xprint


V = {
    'common': {
        'kind': ['c', 'c++', 'linker'],
        'type': 'gcc',
        'version': '9.2',
        'build': [
            '#pragma manual deps',
            '$(FETCH_URL_2)',
            'rm -rf $(BUILD_DIR)/fetched_urls',
            'mv $(BUILD_DIR)/* $(INSTALL_DIR)/'
        ],
        'prepare': [
            'export PATH=$(GCC_BIN_DIR):$PATH',
            'export LDFLAGS="--static $LDFLAGS"',
            'export CFLAGS="-O2 -I$(GCC_INC_DIR) $CFLAGS"',
        ],
        'codec': 'gz',
    },
    "barebone": [
        {
            'prefix': ['tool_native_prefix', 'x86_64-linux-musl-'],
            "url": "https://musl.cc/x86_64-linux-musl-native.tgz",
            "constraint": {
                'host': {
                    'os': 'linux',
                    'arch': 'x86_64',
                },
            },
        },
        {
            'prefix': ['tool_native_prefix', 'aarch64-linux-musl-'],
            "url": "https://musl.cc/aarch64-linux-musl-native.tgz",
            "constraint": {
                'host': {
                    'os': 'linux',
                    'arch': 'aarch64',
                },
            },
        },
        {
            'prefix': ['tool_cross_prefix', 'aarch64-linux-musl-'],
            "url": "https://musl.cc/aarch64-linux-musl-cross.tgz",
            "constraint": {
                'host': {
                    'os': 'linux',
                    'arch': 'x86_64',
                },
                'target': {
                    'arch': 'aarch64',
                },
            },
        },
    ],
}


def fix_constraints(h, t):
    for k, v in h.items():
        if k not in t:
            t[k] = v


def fix_constraints_cc(cc):
    cc = deep_copy(cc)

    if 'target' not in cc:
        cc['target'] = {}

    fix_constraints(cc['host'], cc['target'])

    cc['is_cross'] = is_cross(cc)

    return deep_copy(cc)


def small_repr(c):
    return c['os'] + '-' + c['arch']


def small_repr_cons(c):
    return small_repr(c['host']) + '$' + small_repr(c['target'])


def is_cross(cc):
    return small_repr(cc['host']) != small_repr(cc['target'])


def iter_comp():
    for v in V['barebone']:
        v = deep_copy(v)
        v.update(deep_copy(V['common']))

        v['constraint'] = fix_constraints_cc(v['constraint'])

        yield {
            'node': v,
            'deps': [],
        }


def iter_musl_cc_tools():
    for n in iter_comp():
        nd = store_node(n)

        c = deep_copy(n)
        l = deep_copy(n)

        c['node']['kind'] = 'c/c++'
        c['node']['type'] = 'gcc'

        l['node']['kind'] = 'linker'
        l['node']['type'] = 'binutils'

        for x in (c, l):
            xn = x['node']

            xn.pop('url', None)
            xn.pop('build')
            xn.pop('prepare', None)
            xn['extra_deps'] = [nd]
            xn['name'] = 'muslcc-' + xn['kind'] + '-' + xn['type']

            yield deep_copy(x)


def iter_system_compilers():
    for t in ('gcc', 'clang'):
        tp = y.find_tool(t)

        yield {
            'kind': ['c', 'c++', 'linker'],
            'type': 'clang',
            'name': os.path.basename(tp),
            'path': tp,
            'data': subprocess.check_output([tp, '--version'], stderr=subprocess.STDOUT, shell=False),
        }


def iter_targets(*extra):
    for x in extra:
        yield x

    for a in ('x86_64', 'aarch64'):
        for o in ('linux', 'darwin'):
            yield {
                'arch': a,
                'os': o,
            }


def iter_system_impl():
    def iter_c():
        for c in iter_system_compilers():
            if c['type'] == 'clang':
                yield c

    for c in iter_c():
        data = c.pop('data')

        for l in data.strip().split('\n'):
            l = l.strip()

            if not l:
                continue

            if not l.startswith('Target'):
                continue

            k, v = l.split(':')

            if k != 'Target':
                continue

            a, b, _ = v.strip().split('-')

            host = {
                'arch': a,
                'os': {'apple': 'darwin'}.get(b, platform.system().lower()),
            }

            for t in iter_targets(host):
                c = deep_copy(c)

                cc = {
                    'host': host,
                    'target': t,
                }

                cc['is_cross'] = is_cross(cc)

                c['constraint'] = cc
                c['version'] = '9.0.0'
                c['build'] = []
                c['codec'] = 'gz'

                if cc['is_cross']:
                    c['prefix'] = ['tool_cross_prefix', '']
                    c['prepare'] = ['export CFLAGS="-O2 --target=%s-%s -fno-short-wchar"' % (t['os'], t['arch'])]
                else:
                    c['prefix'] = ['tool_native_prefix', '']
                    c['prepare'] = ['export CFLAGS="-O2"']

                yield {
                    'node': c,
                    'deps': [],
                }


def iter_system_tools():
    for n in iter_system_impl():
        c = deep_copy(n)
        l = deep_copy(n)

        c['node']['kind'] = 'c/c++'
        c['node']['type'] = 'clang'

        l['node']['kind'] = 'linker'
        l['node']['type'] = 'binutils'

        for x in (l, c):
            xn = x['node']

            xn.pop('url', None)
            xn.pop('data', None)
            xn.pop('build')
            xn.pop('prepare', None)
            xn['extra_deps'] = [store_node(n)]
            xn['name'] = 'system-' + xn['kind'] + '-' + xn['type']

            yield deep_copy(x)


def iter_all_nodes():
    for node in iter_comp():
        yield node

    for node in iter_system_impl():
        yield node


@singleton
def compilers_ptr():
    return intern_struct([store_node(x) for x in iter_all_nodes()])


def iter_all_compilers():
    return deref_pointer(compilers_ptr())


def find_compiler(info):
    for d in iter_all_compilers():
        if small_repr_cons(info) == small_repr_cons(restore_node(d)['node']()['constraint']):
            yield d


def join_versions(deps):
    def iter_v():
        for d in deps:
            yield restore_node(d)['node']()['version']

    return '-'.join(iter_v())


@cached()
def find_compiler_id(info):
    for x in find_compiler(info):
        assert x
        return x

    raise Exception('shit happen %s' % info)


@cached()
def find_compilers(info):
    def iter_compilers():
        if is_cross(info):
            host = info['host']

            yield find_compiler_id({'target': host, 'host': host})

        yield find_compiler_id(info)

    return list(iter_compilers())
