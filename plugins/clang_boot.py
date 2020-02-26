@y.package
def clang_boot0():
    info = {'arch': '{arch}', 'os': '{os}', 'libc': 'musl'}
    c = y.restore_node(y.find_compiler_id(info))

    res = c['node']
    #res['deps'] = c['deps']

    res.pop('build')
    res.pop('prepare')
    res.pop('name')
    res.pop('version')

    res['code'] = ''
    res['meta']['repacks'] = {}

    return res
