import os
import sys
import base64
import itertools

from upm_iface import y


def fix_v2(v):
    assert v is not None

    n = v['node']

    if 'codec' not in n:
        n['codec'] = 'xz'

    if 'url' in n:
        if 'pkg_full_name' not in n:
            n['pkg_full_name'] = y.calc_pkg_full_name(n['url'])

    return v


def call_key(func, info):
    return [func.__name__, info]


@y.cached(key=call_key)
def call_v2(func, info):
    if 'compilers' in info:
        param = info
    else:
        compilers = y.find_compilers(info)

        param = {
            'compilers': {
                'deps': y.deep_copy(compilers),
                'cross': len(compilers) > 1,
            },
            'info': info,
        }

    data = func(param)

    if y.is_pointer(data):
        data = y.restore_node_simple(data)

    node = data['node']

    if 'name' not in node:
        node['name'] = func.__name__

    return data


@y.cached()
def to_v2(data, info):
    code = data.get('code', '')
    full = code + '\n' + data.get('prepare', '')

    node = {
        "constraint": info['info'],
    }

    def iter_prepare():
        for l in y.to_lines(data.get('prepare', '')):
            yield l

    node['prepare'] = list(iter_prepare())

    for x in ('version', 'codec', 'extra', 'name'):
        if x in data:
            node[x] = data[x]

    for k in ('src', 'url'):
        if k in data:
            node['url'] = data[k]

    def iter_extra_lines():
        if '$(FETCH_URL' not in full and 'url' in node:
            yield '$(FETCH_URL)'

    def iter_subst():
        for i, v in enumerate(node.get('extra', [])):
            if v['kind'] == 'file':
                cmd = 'echo "' + base64.b64encode(v['data']) + '" | base64 -D -i - -o - > ' + v['path']
                key = '$(APPLY_EXTRA_PLAN_' + str(i) + ')'

                yield (key, cmd)

            if v['kind'] == 'subst':
                yield (v['from'], v['to'])

    node['build'] = list(iter_extra_lines()) + y.to_lines(y.subst_kv_base(code, iter_subst()))

    compilers = info['compilers']['deps']

    if '#pragma cc' not in full:
        if './configure' not in full:
            compilers = []

    return fix_v2({
        'node': node,
        'deps': list(itertools.chain(compilers, data.get('deps', [])))
    })
