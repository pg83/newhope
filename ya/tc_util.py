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


def iter_all_targets_0():
    for a in ('x86_64',):
        yield {
            'arch': a,
            'os': 'darwin',
        }

    for a in ('x86_64'):
        yield {
            'arch': a,
            'libc': 'musl',
            'os': 'linux',
        }

        for libc in ('musl'):
            yield {
                'arch': a,
                'os': 'linux',
                'libc': libc,
            }


def iter_all_targets():
    yield {
        'arch': 'x86_64',
        'libc': 'musl',
        'os': 'linux',
    }


@y.singleton
def rev_target_map():
    res = {}

    for x in iter_all_targets():
        res[small_repr(x)] = x

    return res


def to_full_target(name):
    print name

    return rev_target_map()[name]


def iter_all_arch():
    yield from sorted(frozenset(x['arch'] for x in iter_all_targets()))


def iter_all_os():
    yield from sorted(frozenset(x['os'] for x in iter_all_targets()))


@y.singleton
def current_host_platform():
    res = {
        'arch': y.platform.machine(),
        'os': y.platform.system().lower(),
    }

    if res['os'] == 'linux':
        if 'alpine' in y.platform.uname().version.lower():
            res['libc'] = 'musl'
        else:
            res['libc'] = 'glibc'

    return res
