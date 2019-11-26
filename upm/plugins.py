def dep_name(dep):
    return y.restore_node_node(dep)['name']


def dep_list(info, iter):
    return [x(info) for x in iter]


def parse_line(l):
    if l.startswith('source fetch '):
        return l.split('"')[1]

    return False
