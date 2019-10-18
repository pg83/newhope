import sys
import subprocess
import platform
import os

from .ft import deep_copy, cached, singleton
from .db import store_node, restore_node, deref_pointer, intern_struct


V = {
    'common': {
        'kind': 'c/c++ compiler',
        'name': 'gcc',
        'version': '9.2',
        'build': [
            '#pragma manual deps',
            '$(FETCH_URL_2)',
            'rm -rf $(BUILD_DIR)/fetched_urls',
            'mv $(BUILD_DIR)/* $(INSTALL_DIR)/'
        ],
        "from": __file__,
        'codec': 'gz',
        'prepare': [
            'export PATH=$(GCC_BIN_DIR):$PATH',
            'export LDFLAGS="--static $LDFLAGS"',
            'export CFLAGS="-O2 -I$(GCC_INC_DIR) $CFLAGS"',
        ]
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


def small_repr(c):
    return c['os'] + '-' + c['arch']


def fix_constraints(h, t):
    for k, v in h.items():
        if k not in t:
            t[k] = v


def is_cross(cc):
    return small_repr(cc['host']) != small_repr(cc['target'])


def iter_comp():
    for v in V['barebone']:
        v = deep_copy(v)
        v.update(deep_copy(V['common']))

        cc = v['constraint']

        if 'target' not in cc:
            cc['target'] = {}

        fix_constraints(cc['host'], cc['target'])

        cc['is_cross'] = is_cross(cc)

        yield {
            'node': v,
            'deps': [],
        }


def is_compat_x(info, comp_node):
    for k in info:
        if k not in comp_node:
            return False

        if info[k] != comp_node[k]:
            return False

    return True


def is_compat(info, comp_node):
    return is_compat_x(info.get('constraint', info), comp_node.get('constraint', comp_node))


@cached(key=lambda x: x)
def find_tool(name):
    return subprocess.check_output(['echo `which ' + name + '`'], shell=True).strip()


def iter_system_compilers():
    for t in ('gcc', 'clang'):
        try:
            tp = find_tool(t)

            if tp:
                yield {
                    'kind': 'clang',
                    'name': os.path.basename(tp),
                    'path': tp,
                    'data': subprocess.check_output([tp, '--version'], stderr=subprocess.STDOUT, shell=False),
                    'codec': 'gz',
                }
        except Exception as e:
            print >>sys.stderr, e


def iter_targets(*extra):
    for x in extra:
        yield x

    for a in ('x86_64', 'aarch64'):
        for o in ('linux',):
            for l in ('musl', 'uclibc'):
                yield {
                    'arch': a,
                    'os': o,
                    'libc': l,
                }

        for o in ('darwin',):
            yield {
                'arch': a,
                'os': o,
            }


def iter_system_impl():
    for c in iter_system_compilers():
        if c['kind'] == 'clang':
            data = c.pop('data')

            for l in data.strip().split('\n'):
                l = l.strip()

                if l:
                    if not l.startswith('Target'):
                        continue

                    k, v = l.split(':')

                    if k == 'Target':
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

                            if cc['is_cross']:
                                c['prefix'] = ['tool_cross_prefix', '']
                                c['prepare'] = ['export CFLAGS="-O2 -target=%s-%s -fno-short-wchar"' % (t['os'], t['arch'])]
                            else:
                                c['prefix'] = ['tool_native_prefix', '']
                                c['prepare'] = ['export CFLAGS="-O2"']

                            yield {
                                'node': c,
                                'deps': [],
                            }
        else:
            print >>sys.stderr, 'drop', c


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
        node = restore_node(d)

        if is_compat(info, node['node']()):
            yield d
