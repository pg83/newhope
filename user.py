import os
import sys
import subprocess
import json
import gen_id

def fp(f, v, *args, **kwargs):
    def wrap(*args, **kwargs):
        return f(v, *args, **kwargs)

    return wrap


from cc import find_compiler
from gen_id import to_visible_name, cur_build_system_version, deep_copy
from bb import find_busybox


def singleton(f):
    def wrapper():
        try:
            f.__res
        except AttributeError:
            f.__res = f()

        return f.__res

    return wrapper


def cached(f):
    v = {}

    def wrapper(*args, **kwargs):
        k = gen_id.struct_dump([args, kwargs])

        if f not in v:
            v[k] = f(*args, **kwargs)

        return deep_copy(v[k])

    return wrapper


@singleton
def current_host_platform():
    data = subprocess.check_output(['/bin/uname', '-a'], shell=False).strip();

    for x in ('aarch64', 'x86_64'):
        if x in data:
            return x

    return data.split()[-1]


@cached
def find_compiler_id(info):
    info = gen_id.deep_copy(info)

    info.pop('build_system_version')

    for x in find_compiler(info):
        return x

    raise Exception('shit happen')


def is_cross(info):
    return info['target'] != info['host']


def subst_info(info):
    info = json.loads(json.dumps(info))

    if 'host' not in info:
        info['host'] = current_host_platform()

    if 'target' not in info:
        info['target'] = 'aarch64'

    if 'libc' not in info:
        info['libc'] = 'musl'

    if 'build_system_version' not in info:
        info['build_system_version'] = cur_build_system_version()

    return info


USER_FUNCS = []


def helper(func):
    def wrapper(info):
        name = func.__name__
        wrapper.__name__ = name
        info = subst_info(info)

        def iter_compilers():
            if is_cross(info):
                cinfo = json.loads(json.dumps(info))
                cinfo['target'] = cinfo['host']

                yield find_compiler_id(cinfo)

            yield find_compiler_id(info)

        compilers = list(iter_compilers())

        try:
            full_data = func()
        except TypeError:
            full_data = func({'compilers': compilers, 'info': info})

        data = full_data['code']
        src = full_data['src']

        def iter_compilers():
            if '#pragma cc' not in data:
                return []

            return compilers

        deps = list(iter_compilers())

        if deps:
            cross_cc = deps[-1]
        else:
            cross_cc = None

        def iter_extra_lines():
            if cross_cc:
                yield 'ln -sf `which ' + cross_cc['node']['prefix'][1] + 'gcc` /bin/cc'

            if '$(FETCH_URL' not in data:
                yield '$(FETCH_URL)'

        return {
            'node': {
                'name': func.__name__,
                "url": src,
                "constraint": info,
                "from": 'plugins/' + func.__name__ + '.py',
                'build': list(iter_extra_lines()) + [x.strip() for x in data.split('\n')],
            },
            'deps': deps,
        }

    USER_FUNCS.append((wrapper.__name__, wrapper))

    return wrapper


def find_busybox_ex(info):
    return find_busybox(info['host'], info['target'])


def add_tool_deps(pkg, data):
    def iter_tools():
        for k, v in USER_FUNCS:
            kk = '$(' + k.upper() + '_'

            if kk in data:
                cc = json.loads(json.dumps(pkg['constraint']))
                cc['host'] = cc['target']

                yield v(cc)

    return list(iter_tools())


def gen_packs(host=current_host_platform(), targets=['x86_64', 'aarch64']):
    for name, func in USER_FUNCS:
        for target in targets:
            yield func({'target': target, 'host': host})


def load_plugins(where):
    for x in os.listdir(where):
        if '~' not in x and '#' not in x:
            with open(where + '/' + x, 'r') as f:
                exec(f, globals(), locals())
