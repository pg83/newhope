import os
import sys
import base64
import itertools


def call_v2(func, info):
    if 'compilers' in info:
        param = info
    else:
        if info:
            compilers = y.find_compilers(info)
        else:
            compilers = []

        param = {
            'compilers': {
                'deps': y.deep_copy(compilers),
                'cross': len(compilers) > 1,
            },
            'info': info,
        }

    data = func(param)

    if y.is_pointer(data):
        data = y.deep_copy(y.restore_node(data))

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
        p = data.get('prepare', '')

        for l in y.to_lines(p):
            yield l

    node['prepare'] = list(iter_prepare())

    for x in ('version', 'codec', 'extra', 'name', 'do_fetch_node', 'pkg_full_name', 'inputs', 'output', 'meta'):
        if x in data:
            node[x] = data[x]

    def iter_subst():
        for i, v in enumerate(node.get('extra', [])):
            if v['kind'] == 'file':
                cmd = 'echo "' + base64.b64encode(v['data']) + '" | (base64 -D -i - -o - || base64 -d) > ' + v['path']
                key = '$(APPLY_EXTRA_PLAN_' + str(i) + ')'

                yield (key, cmd)

            if v['kind'] == 'subst':
                yield (v['from'], v['to'])

    node['build'] = y.to_lines(y.subst_kv_base(code, iter_subst()))

    compilers = info['compilers']['deps']

    if '#pragma cc' not in full:
        if './configure' not in full:
            compilers = []

    return y.fix_v2({
        'node': node,
        'deps': list(itertools.chain(compilers, data.get('deps', [])))
    })
