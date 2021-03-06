def cons_to_name_x(c):
    if not c:
        return 'nop'

    try:
        c = c['target']
    except KeyError:
        pass

    res = ''

    for k, f in (('os', 1), ('libc', 1), ('arch', 2)):
        if k in c:
            res += c[k][:f]

    return res


def small_repr(c):
    return cons_to_name_x(c)


def iter_all_targets():
    for a in ('x86_64',):
        yield {
            'arch': a,
            'os': 'darwin',
        }

    for a in ('x86_64',):
        for libc in ('musl',):
            yield {
                'arch': a,
                'os': 'linux',
                'libc': libc,
            }


@y.singleton
def rev_target_map():
    res = {}

    for x in iter_all_targets():
        res[small_repr(x)] = x

    return res


def to_full_target(name):
    return rev_target_map()[name]
