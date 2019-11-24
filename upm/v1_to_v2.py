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

    return data


@y.cached()
def to_v2(data, info):
    node = y.copy.copy(data)
    node.pop('deps', None)

    code = node.pop('code', '')
    prepare = node.pop('prepare', '')
    full = '\n'.join((code, prepare))

    node['constraint'] = info['info']
    node['prepare'] = y.to_lines(prepare)

    if 'meta' not in node:
        node['meta'] = {}
        
    meta = node['meta']

    if 'kind' not in meta:
        meta['kind'] = node.pop('kind', [])

    def iter_subst():
        for i, v in enumerate(node.get('extra', [])):
            if v['kind'] == 'file':
                cmd = 'echo "' + base64.b64encode(v['data'].encode('utf-8')).decode('utf-8') + '" | (base64 -D -i - -o - || base64 -d) > ' + v['path']
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
