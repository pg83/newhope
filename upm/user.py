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


def v1_to_v2_key(func, info):
    return [func.__name__, info]


@cached(key=v1_to_v2_key)
def v1_to_v2(func, info):
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

    return {'node': node, 'deps': list(iter_deps())}


def move_many(fr, dirs):
    return '\n'.join([('cp -R %s $(INSTALL_DIR)/' % (fr + x)) for x in dirs]) + '\n'

