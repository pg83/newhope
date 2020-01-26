import os
import sys
import base64
import itertools


def call_v2(func):
    data = func()

    if y.is_pointer(data):
        data = y.restore_node(data)

    return data


@y.cached()
def to_v2(data, info):
    print data, info
    node = y.copy.copy(data)
    node.pop('deps', None)

    code = node.pop('code', '')
    prepare = node.pop('prepare', '')
    full = '\n'.join((code, prepare))

    node['constraint'] = info
    node['prepare'] = y.to_lines(prepare)
    node['build'] = y.to_lines(code)

    if all((y not in full) for y in ('#pragma cc', './configure', 'YMAKE', '$CC', '$CXX', 'gcc', 'clang')):
        compilers = []
    else:
        compilers = y.find_compilers(info)

    return y.fix_v2({
        'node': node,
        'deps': list(itertools.chain(compilers, data.get('deps', [])))
    })
