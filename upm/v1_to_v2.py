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
    node['build'] = y.to_lines(code)
    
    compilers = info['compilers']['deps']

    if all((y not in full) for y in ('#pragma cc', './configure', 'YMAKE', '$CC', '$CXX', 'gcc', 'clang')):
        compilers = []

    return y.fix_v2({
        'node': node,
        'deps': list(itertools.chain(compilers, data.get('deps', [])))
    })
