import os
import sys


from upm_iface import y


def calc_pkg_full_name(url):
    if url.endswith('download'):
        url = os.path.dirname(url)

    return os.path.basename(url)


def cons_to_name_1(c, func=lambda x: a, delim='-'):
    if not c:
        return 'noarch'

    def iter_parts():
        for k in ('os', 'libc', 'arch'):
            if k in c:
                yield func(c[k])

    return delim.join(iter_parts())


def short_const_1(c):
    return cons_to_name_1(c, func=lambda x: x[0], delim='')


def cons_to_name_2(c, func=lambda x: a, delim='-'):
    if not c:
        return 'noarch'

    r1 = cons_to_name_1(c['host'], func, delim)
    r2 = cons_to_name_1(c['target'], func, delim)

    if r1 == r2:
        return r1

    return r1 + r2


def short_const_2(c):
    return cons_to_name_2(c, func=lambda x: x[0], delim='')


def remove_compressor_name(x):
    for i in ('.tgz', '.tbz', '.txz', '.gz', '.bz2', '.xz', '.tar'):
        if x.endswith(i):
            x = x[0:len(x) - len(i)]

    return x


def to_visible_name_0(pkg):
    def iter_parts():
        name = pkg['name']

        yield pkg['good_id'][:8]
        yield short_const_2(pkg.get('constraint'))

        def pkg_name():
            if 'version' in pkg:
                return name + pkg['version']
            elif 'url' in pkg:
                return remove_compressor_name(calc_pkg_full_name(pkg['url']))
            else:
                return name

        yield pkg_name().replace('-', '').replace('_','').replace('.', '')

    return '-'.join(iter_parts()).replace('_', '-').replace('.', '-').replace('--', '-')


def to_visible_name_1(pkg):
    res = to_visible_name_0(pkg)
    codec = pkg['codec']
    res = res[:8] + '-' + codec + res[8:]

    if res.endswith('//'):
        res = res[:-1]

    return res


def to_visible_name_2(pkg):
    return to_visible_name_1(pkg)


def to_visible_name_3(pkg, good_id=None):
    res = {}

    for k in ('codec', 'version', 'url', 'constraint', 'name'):
        if k in pkg:
            res[k] = pkg[k]

    if good_id:
        res['good_id'] = good_id

    return to_visible_name_2(res)


def to_visible_name_4(root):
    try:
        to_visible_name_4.__cache
    except AttributeError:
        to_visible_name_4.__cache = {}

    c = to_visible_name_4.__cache
    good_id = root['noid']

    if good_id not in c:
        c[good_id] = to_visible_name_3(root['node'](), good_id=good_id).lower()

    return c[good_id]


FUNCS = [
    to_visible_name_0,
    to_visible_name_1,
    to_visible_name_2,
    to_visible_name_3,
    to_visible_name_4,
]


def cur_build_system_version():
    return len(FUNCS) - 1


y.logged_wrapper
def to_visible_name(root):
    return FUNCS[cur_build_system_version()](root)
