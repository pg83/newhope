import os
import sys
import platform
import json
import functools


def fp(f, v, *args, **kwargs):
    def wrap(*args, **kwargs):
        return f(v, *args, **kwargs)

    return wrap


from .cc import find_compiler
from .gen_id import to_visible_name, cur_build_system_version, deep_copy, struct_dump


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
        k = struct_dump([args, kwargs])

        if f not in v:
            v[k] = f(*args, **kwargs)

        return deep_copy(v[k])

    return wrapper


@singleton
def current_host_platform():
    return platform.machine()


@cached
def find_compiler_id(info):
    info = deep_copy(info)

    info.pop('build_system_version')

    for x in find_compiler(info):
        return x

    raise Exception('shit happen')


@cached
def find_compilers(info):
    def iter_compilers():
        if is_cross(info):
            cinfo = deep_copy(info)
            cinfo['target'] = cinfo['host']

            yield find_compiler_id(cinfo)

        yield find_compiler_id(info)

    return list(iter_compilers())


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


def simple_funcs():
    for k, v in USER_FUNCS:
        if k.startswith('orig_'):
            pass
        else:
            yield k, v


def gen_by_name(n):
    for k, v in simple_funcs():
        if k == n:
            return v

    raise Exception('shit happen')


def gen_by_name_priv(n):
    for k, v in USER_FUNCS:
        if k == n:
            return v

    raise Exception('shit happen')


def to_lines(text):
    def iter_l():
        for l in text.split('\n'):
            l = l.strip()

            if l:
                yield l

    return list(iter_l())


def helper(func):
    @functools.wraps(func)
    def wrapper(info):
        info = subst_info(info)
        compilers = find_compilers(info)

        try:
            full_data = func()
        except TypeError:
            full_data = func({'compilers': compilers, 'info': info, 'generator_func': gen_by_name_priv})

        data = full_data['code']

        if '#pragma cc' not in data:
            compilers = []

        node = {
            'name': func.__name__,
            "constraint": info,
            "from": 'plugins/' + func.__name__ + '.py',
        }

        if 'prepare' in full_data:
            node['prepare'] = to_lines(full_data['prepare'])

        if 'version' in full_data:
            node['version'] = full_data['version']

        if 'codec' in full_data:
            node['codec'] = full_data['codec']

        for k in ('src', 'url'):
            if k in full_data:
                node['url'] = full_data[k]

        def iter_extra_lines():
            if compilers:
                yield 'ln -sf `which ' + compilers[-1]['node']['prefix'][1] + 'gcc` /bin/cc'

            if '$(FETCH_URL' not in data and 'url' in node:
                yield '$(FETCH_URL)'

        node['build'] = list(iter_extra_lines()) + to_lines(data)

        return {
            'node': node,
            'deps': compilers + full_data.get('deps', []),
        }

    USER_FUNCS.append((wrapper.__name__, wrapper))
    USER_FUNCS.append(('orig_' + wrapper.__name__, func))

    return wrapper


def add_tool_deps(pkg, data):
    def iter_tools():
        for k, v in simple_funcs():
            kk = '$(' + k.upper() + '_'

            if kk in data:
                cc = json.loads(json.dumps(pkg['constraint']))
                cc['host'] = cc['target']

                yield v(cc)

    return list(iter_tools())


def gen_packs(host=current_host_platform(), targets=['x86_64', 'aarch64']):
    for name, func in simple_funcs():
        for target in targets:
            yield func({'target': target, 'host': host})


def load_plugins(where, kof):
    def iter_plugins():
        for x in sorted(os.listdir(where)):
            if '~' not in x and '#' not in x:
                yield where + '/' + x

    def load_one_plugin(xx):
        with open(xx, 'r') as f:
            try:
                exec(f, globals(), locals())
            except Exception as e:
                s = 'can not load %s, cause %s' %(xx, e)

                if kof:
                    print >>sys.stderr, s
                else:
                    raise Exception(s)

    for x in iter_plugins():
        load_one_plugin(x)
