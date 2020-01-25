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


def small_repr_cons(c):
    return small_repr(c.get('host', c['target'])) + '$' + small_repr(c['target'])


def is_cross(cc):
    if not cc:
        return False

    return small_repr(cc['host']) != small_repr(cc['target'])


def subst_info(info):
    info = y.dc(info)

    if 'host' not in info:
        info['host'] = current_host_platform()

    if 'target' not in info:
        info['target'] = y.dc(info['host'])

    return info


def iter_all_targets():
    for a in ('x86_64', 'aarch64', 'arm', 'armv7a', 'i686'):
        yield {
            'arch': a,
            'os': 'linux',
        }

        for libc in ('glibc', 'musl', 'uclibc'):
            yield {
                'arch': a,
                'os': 'linux',
                'libc': libc,
            }

    for a in ('x86_64',):
        yield {
            'arch': a,
            'os': 'darwin',
        }


@y.singleton
def rev_target_map():
    res = {}

    for x in iter_all_targets():
        res[small_repr(x)] = x

    print res

    return res


def to_full_target(name):
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
