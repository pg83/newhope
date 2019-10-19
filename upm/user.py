import os
import imp
import sys
import json
import base64
import platform
import functools
import itertools

from .ft import singleton, cached, fp, deep_copy
from .cc import find_compiler, is_cross, iter_targets, find_compilers
from .gen_id import to_visible_name, calc_pkg_full_name
from .xpath import xp
from .db import restore_node, store_node, pointer, deref_pointer, intern_struct
from .subst import subst_kv_base
from .ndk import iter_android_ndk_20
from .helpers import current_host_platform, subst_info, to_lines


USER_FUNCS_BY_NAME = {}


def simple_funcs():
    for k in sorted(USER_FUNCS_BY_NAME.keys()):
        yield k, USER_FUNCS_BY_NAME[k][0]


@cached(key=lambda x: x)
def real_wrapper(func_name, info):
    func = USER_FUNCS_BY_NAME[func_name][1]
    info = subst_info(info)
    compilers = find_compilers(info)

    try:
        full_data = func()
    except TypeError:
        param = {
            'compilers': {
                'deps': deep_copy(compilers),
                'cross': len(compilers) > 1,
            },
            'info': info,
        }

        full_data = func(param)

    try:
        data = full_data['code']
    except TypeError:
        return full_data
    except KeyError:
        return full_data

    if '#pragma cc' not in data:
        if './configure' not in data:
            compilers = []

    node = {
        'name': func.__name__,
        "constraint": info,
        "from": func.__name__ + '.py',
    }

    def iter_prepare():
        for l in to_lines(full_data.get('prepare', '')):
            yield l

    node['prepare'] = list(iter_prepare())
    node['codec'] = 'xz'

    for x in ('version', 'codec', 'extra'):
        if x in full_data:
            node[x] = full_data[x]

    for k in ('src', 'url'):
        if k in full_data:
            node['url'] = full_data[k]
            node['pkg_full_name'] = calc_pkg_full_name(node['url'])

    def iter_extra_lines():
        if '$(FETCH_URL' not in data and 'url' in node:
            yield '$(FETCH_URL)'

    def iter_subst():
        for i, v in enumerate(node.get('extra', [])):
            if v['kind'] == 'file':
                cmd = 'echo "' + base64.b64encode(v['data']) + '" | base64 -D -i - -o - > ' + v['path']
                key = '$(APPLY_EXTRA_PLAN_' + str(i) + ')'

                yield (key, cmd)

            if v['kind'] == 'subst':
                yield (v['from'], v['to'])

    node['build'] = list(iter_extra_lines()) + to_lines(subst_kv_base(data, iter_subst()))

    def iter_deps():
        for x in compilers:
            if x:
                yield x

        for x in full_data['deps']:
            if x:
                yield x

    lst = list(iter_deps())

    assert None not in lst

    return store_node({'node': node, 'deps': lst})


def helper(func):
    @functools.wraps(func)
    def wrapper(info):
        if 'info' in info:
            info = info['info']

        return real_wrapper(func.__name__, info)

    USER_FUNCS_BY_NAME[wrapper.__name__] = (wrapper, func)

    return wrapper


def move_many(fr, dirs):
    return '\n'.join([('cp -R %s $(INSTALL_DIR)/' % (fr + x)) for x in dirs]) + '\n'


def gen_packs_1(host=current_host_platform(), targets=['x86_64', 'aarch64'], os=['linux', 'darwin'], funcs=[]):
    for func in funcs:
        for target in targets + [host]:
            yield func({'host': host, 'target': target})

    for name, func in simple_funcs():
        for target in iter_targets(host):
            yield func({'host': host, 'target': target})

    for x in iter_android_ndk_20():
        yield x


def gen_packs(extra_funcs=[], host=current_host_platform(), targets=['x86_64', 'aarch64'], os=['linux', 'darwin']):
    for x in gen_packs_1(host, targets, os, funcs=extra_funcs):
        if x:
            yield x
