def call_v2(func):
    data = func()

    if y.is_pointer(data):
        data = y.restore_node(data)

    return data


@y.cached
def to_v2(data, info):
    node = y.copy.copy(data)

    deps = node.pop('deps', [])
    code = node.pop('code', '')
    prepare = node.pop('prepare', '')

    node['host'] = info
    node['prepare'] = y.to_lines(prepare)
    node['build'] = y.to_lines(code)

    return y.fix_v2({
        'node': node,
        'deps': deps,
    })
