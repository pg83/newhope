def dep_name(dep):
    return y.restore_node_node(dep)['name']


def dep_list(info, iter):
    return [x(info) for x in iter]


@y.gd_callback('new plugin')
def exec_plugin_code(code):
    name = code['name']
    name = name.replace('/', '.')

    if name.endswith('.py'):
        name = name[:-3]

    __yexec__(code['data'], module_name=name)


def parse_line(l):
    if l.startswith('source fetch '):
        return l.split('"')[1]

    return False



