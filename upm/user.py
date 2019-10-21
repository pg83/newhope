import os
import sys
import base64
import functools
import itertools

from upm_ft import singleton, cached, fp, deep_copy
from upm_cc import find_compilers
from upm_subst import subst_kv_base
from upm_helpers import subst_info, to_lines
from upm_iface import y


def v1_to_v2_key(func, info):
    return [func.__name__, info]


@cached(key=v1_to_v2_key)
def v1_to_v2(func, info):
    compilers = find_compilers(info)

    param = {
        'compilers': {
            'deps': deep_copy(compilers),
            'cross': len(compilers) > 1,
        },
        'info': info,
    }

    full_data = func(param)

    #y.debug_print(full_data)

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
    }

    def iter_prepare():
        for l in to_lines(full_data.get('prepare', '')):
            yield l

    node['prepare'] = list(iter_prepare())

    for x in ('version', 'codec', 'extra'):
        if x in full_data:
            node[x] = full_data[x]

    for k in ('src', 'url'):
        if k in full_data:
            node['url'] = full_data[k]

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

    return {
        'node': node,
        'deps': list(itertools.chain(compilers, full_data['deps']))
    }
