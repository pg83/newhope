import os


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


def to_visible_name_0(pkg, good_id):
    def iter_parts():
        yield pkg['name'].replace('_', '')
        yield cons_to_name_x(pkg.get('constraint'))
        yield 'v4' + good_id[:10][2:]
        yield pkg['codec']

    return '-'.join(iter_parts())


def to_visible_name_4(root):
    key = y.calc_noid(root)

    try:
        return root[key]
    except KeyError:
        root[key] = to_visible_name_0(root['node'], good_id=key).lower()

    return root[key]


def to_visible_name(root):
    return root['trash']['replacer'](to_visible_name_4(root))


def to_pretty_name(t):
    if len(t) < 10:
        return t
    
    t = t[4:]
    t = t[:t.find('-v5')]

    return t
