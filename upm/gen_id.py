import os
import sys
import json
import hashlib


from .ft import struct_dump, deep_copy, cached


def cons_to_name(c):
    if not c:
        return 'noarch'

    def iter_parts():
        if c['host'] != c['target']:
            yield c['host']

        yield c['libc']
        yield c['target']

    return '-'.join(iter_parts())


def remove_compressor_name(x):
    for i in ('.tgz', '.tbz', '.txz', '.gz', '.bz2', '.xz', '.tar'):
        if x.endswith(i):
            x = x[0:len(x) - len(i)]

    return x


def to_visible_name_0(pkg):
    def iter_parts():
        name = pkg['name']

        yield pkg['good_id'][:8]
        yield cons_to_name(pkg.get('constraint'))
        yield name

        if 'version' in pkg:
            yield pkg['version']
        elif 'url' in pkg:
            p = remove_compressor_name(os.path.basename(pkg['url']))

            for n in (name, name[:-1]):
                if p.startswith(n):
                    p = p[len(n):]

                    break

            yield p

    return '-'.join(iter_parts()).replace('_', '-').replace('.', '-').replace('--', '-')


def to_visible_name_1(pkg):
    res = to_visible_name_0(pkg)

    if 'codec' in pkg:
        codec = pkg['codec']
    elif '-noarch-' in res:
        codec = 'tr'
    else:
        codec = 'xz'

    res = res[:8] + '-' + codec + res[8:]

    if res.endswith('//'):
        res = res[:-1]

    return res


@cached
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
    return to_visible_name_3(root['node'](), good_id=root['noid'])


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
    node = root['node']()

    return FUNCS[node.get('constraint', {}).get('build_system_version', cur_build_system_version())](root)
