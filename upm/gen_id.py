import os
import sys
import json
import hashlib


def gen_id(s):
    return hashlib.md5(json.dumps([s, 2], sort_keys=True, indent=4)).hexdigest()


def deep_copy(x):
    return json.loads(json.dumps(x))


def struct_dump(p):
    return hashlib.md5(json.dumps(p, sort_keys=True, indent=4)).hexdigest()


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

        yield gen_id(pkg)[:8]
        yield cons_to_name(pkg.get('constraint'))
        yield name

        if 'url' in pkg:
            p = remove_compressor_name(os.path.basename(pkg['url']))

            for n in (name, name[:-1]):
                if p.startswith(n):
                    p = p[len(n):]

                    break

            yield p
        else:
            if 'version' in pkg:
                yield pkg['version']

    try:
        return '-'.join(iter_parts()).replace('_', '-').replace('.', '-').replace('--', '-')
    except:
        print >>sys.stderr, pkg
        raise


def to_visible_name_1(pkg):
    return to_visible_name_0(pkg)


def to_visible_name_2(pkg):
    res = to_visible_name_1(pkg)

    if 'codec' in pkg:
        codec = pkg['codec']
    elif '-noarch-' in res:
        codec = 'tr'
    elif '-busybox-' in res or '-xz-' in res or '-linux-musl-' in res or '-mbedtls-' in res:
        codec = 'gz'
    else:
        codec = 'xz'

    res = res[:8] + '-' + codec + res[8:]

    if res.endswith('//'):
        res = res[:-1]

    return res


FUNCS = [
    to_visible_name_0,
    to_visible_name_1,
    to_visible_name_2,
]


def cur_build_system_version():
    return len(FUNCS) - 1


def to_visible_name(pkg):
    cc = pkg.get('constraint', {})
    num = cc.get('build_system_version', cur_build_system_version())

    return FUNCS[num](pkg)
