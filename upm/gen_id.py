import os
import sys


def calc_pkg_full_name(url):
    if url.endswith('download'):
        url = os.path.dirname(url)

    return os.path.basename(url)


def cons_to_name_1(c, func=lambda x: x, delim='-'):
    if not c:
        return 'noarch'

    def iter_parts():
        for k in ('os', 'libc', 'arch'):
            if k in c:
                yield func(c[k])

    return delim.join(iter_parts())


def short_const_1(c):
    return cons_to_name_1(c, func=lambda x: x[:2], delim='-')


def cons_to_name_2(c, func=lambda x: x, delim='-'):
    if not c:
        return 'noarch'

    r1 = cons_to_name_1(c['host'], func, delim)
    r2 = cons_to_name_1(c['target'], func, delim)

    if r1 == r2:
        return r1

    return r1 + '-' + r2


def cons_to_name_x(c):
    if not c:
        return 'nop'

    c = c['target']
    res = ''

    for k, f in (('os', 1), ('libc', 1), ('arch', 2)):
        if k in c:
            res += c[k][:f]
            
    return res


def short_const_2(c):
    return cons_to_name_2(c, func=lambda x: x[:2], delim='')


def remove_compressor_name(x):
    for i in ('.tgz', '.tbz', '.txz', '.gz', '.bz2', '.xz', '.tar'):
        if x.endswith(i):
            x = x[0:len(x) - len(i)]

    return x


def to_visible_name_0(pkg):
    def iter_parts():
        yield pkg['name']
        yield cons_to_name_x(pkg.get('constraint'))
        yield 'v4' + pkg['good_id'][:10][2:]

    return '-'.join(iter_parts()).replace('_', '-')


def to_visible_name_1(pkg):
    res = to_visible_name_0(pkg)
    codec = pkg['codec']
    res = res + '-' + codec

    return res


def to_visible_name_2(pkg):
    return to_visible_name_1(pkg)


def to_visible_name_3(pkg, good_id=None):
    res = {}

    for k in ('codec', 'constraint', 'name'):
        if k in pkg:
            res[k] = pkg[k]

    if good_id:
        res['good_id'] = good_id

    return to_visible_name_2(res)


def to_visible_name_4(root):
    key = y.calc_noid(root)

    try:
        return root[key]
    except KeyError:
        root[key] = to_visible_name_3(root['node'], good_id=key).lower()

    return root[key]


FUNCS = [
    to_visible_name_0,
    to_visible_name_1,
    to_visible_name_2,
    to_visible_name_3,
    to_visible_name_4,
]


def cur_build_system_version():
    return len(FUNCS) - 1


def to_visible_name(root):
    return root['trash']['replacer'](FUNCS[cur_build_system_version()](root))
