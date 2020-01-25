import os


def calc_pkg_full_name(url):
    if url.endswith('download'):
        url = os.path.dirname(url)

    return os.path.basename(url)


def remove_compressor_name(x):
    for i in ('.tgz', '.tbz', '.txz', '.gz', '.bz2', '.xz', '.tar'):
        if x.endswith(i):
            x = x[0:len(x) - len(i)]

    return x


def to_visible_name_0(pkg, good_id):
    def iter_parts():
        yield pkg['name'].replace('_', '')
        yield y.small_repr(pkg.get('constraint'))
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

    p = t.find('-v5')

    if p < 0:
        return t

    t = t[:p]

    return t
