import os
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

    return '-'.join([c['host'], c['libc'], c['target']])


def to_visible_name_0(pkg):
    return (gen_id(pkg)[:8] + '-' + cons_to_name(pkg.get('constraint')) + '-' + (pkg['name'] + '-' + os.path.basename(pkg.get('url', ''))).replace('_', '-').replace('.', '-')).replace('--', '-')


def to_visible_name_1(pkg):
    def remove_compressor_name(x):
        for i in ('-tgz', '-tbz', '-txz', '-gz', '-bz2', '-xz', '-tar'):
            if x.endswith(i):
                x = x[0:len(x) - len(i)]

        return x

    return remove_compressor_name(to_visible_name_0(pkg))


def to_visible_name_2(pkg):
    res = to_visible_name_1(pkg)

    if '-noarch-' in res:
        codec = 'tar'
    elif '-busybox-' in res or '-xz-' in res or '-linux-musl-' in res or '-mbedtls-' in res:
        codec = 'gz'
    else:
        codec = 'xz'

    return res[:8] + '-' + codec + res[8:]


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
