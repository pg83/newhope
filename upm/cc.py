import sys
import subprocess
import platform
import os

from .ft import deep_copy, cached, singleton
from .db import store_node, restore_node, deref_pointer, intern_struct
from .ndk import find_android_linker_by_cc
from .xpath import xp
from .helpers import xprint


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


def small_repr_cons(c):
    return small_repr(c['host']) + '$' + small_repr(c['target'])


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
                    'codec': 'xz',
                }
        except Exception as e:
            xprint(e)


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
            if c['kind'] == 'clang':
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

                oc = c

                for l in find_android_linker_by_cc(cc, small_repr_cons):
                    c  = deep_copy(oc)

                    c['extra_deps'] = [l]

                    yield {
                        'node': c,
                        'deps': [l],
                    }


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
            yield


def join_versions(deps):
    def iter_v():
        for d in deps:
            yield xp('/d/node/version')

    return '-'.join(iter_v())


@cached(key=lambda x: x)
def find_compiler_id(info):
    for x in find_compiler(info):
        return x

    raise Exception('shit happen %s' % info)


@cached(key=lambda x: x)
def find_compilers(info):
    def iter_compilers():
        if is_cross(info):
            cinfo = deep_copy(info)
            cinfo['target'] = cinfo['host']

            yield find_compiler_id(cinfo)

        yield find_compiler_id(info)

    return list(iter_compilers())
