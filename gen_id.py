import os
import json
import hashlib


def gen_id(s):
    return hashlib.md5(json.dumps([s, 2], sort_keys=True, indent=4)).hexdigest()


def deep_copy(x):
    return json.loads(json.dumps(x))


def cons_to_name(c):
    return '-'.join([c['host'], c['libc'], c['target']])


def to_visible_name_0(pkg):
    return (gen_id(pkg)[:8] + '-' + cons_to_name(pkg['constraint']) + '-' + os.path.basename(pkg['url']).replace('_', '-').replace('.', '-')).replace('--', '-')


def to_visible_name_1(pkg):
    def remove_compressor_name(x):
        for i in ('_tar_', '_tgz', '_tbz', '_txz'):
            p = x.find(i)

            if p > 0:
                x = x[:p]

        return x

    return remove_compressor_name(to_visible_name_0(pkg))


def to_visible_name_2(pkg):
    res = to_visible_name_1(pkg)

    if '-busybox-' in res or '-xz-' in res or '-linux-musl-' in res:
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
    return FUNCS[pkg['constraint']['build_system_version']](pkg)
