import os
import imp
import sys
import platform
import json
import functools


from .ft import singleton, cached, fp, deep_copy, struct_dump
from .cc import find_compiler
from .gen_id import to_visible_name, cur_build_system_version
from .xpath import xp
from .db import restore_node, store_node


def join_versions(deps):
    def iter_v():
        for d in deps:
            yield xp('/d/node/version')

    return '-'.join(iter_v())


@singleton
def current_host_platform():
    return platform.machine()


@cached
def find_compiler_id(info):
    info = deep_copy(info)

    info.pop('build_system_version')

    for x in find_compiler(info):
        return store_node(x)

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
    info = deep_copy(info)

    if 'host' not in info:
        info['host'] = current_host_platform()

    if 'target' not in info:
        info['target'] = 'aarch64'

    if 'libc' not in info:
        info['libc'] = 'musl'

    if 'build_system_version' not in info:
        info['build_system_version'] = cur_build_system_version()

    return info


USER_FUNCS_BY_NAME = {}


@singleton
def simple_funcs():
    def do_iter():
        for k in sorted(USER_FUNCS_BY_NAME.keys()):
            yield k, USER_FUNCS_BY_NAME[k][0]

    return list(do_iter())


def to_lines(text):
    def iter_l():
        for l in text.split('\n'):
            l = l.strip()

            if l:
                yield l

    return list(iter_l())


@cached
def real_wrapper(func_name, info):
    func = USER_FUNCS_BY_NAME[func_name][1]
    info = subst_info(info)
    compilers = find_compilers(info)

    try:
        full_data = func()
    except TypeError:
        param = {
            'compilers': {
                'deps': compilers,
                'cross': len(compilers) > 1,
            },
            'info': info,
        }

        full_data = func(param)

    data = full_data['code']

    if '#pragma cc' not in data:
        if './configure' not in data:
            compilers = []

    node = {
        'name': func.__name__,
        "constraint": info,
        "from": func.__name__ + '.py',
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
            cnode = restore_node(compilers[-1])

            yield 'ln -sf `which ' + cnode['node']()['prefix'][1] + 'gcc` /bin/cc'

        if '$(FETCH_URL' not in data and 'url' in node:
            yield '$(FETCH_URL)'

    node['build'] = list(iter_extra_lines()) + to_lines(data)

    def iter_deps():
        for x in compilers:
            yield x

        for x in full_data.get('deps', []):
            yield x

    return store_node({'node': node, 'deps': list(iter_deps())})


def helper(func):
    @functools.wraps(func)
    def wrapper(info):
        if 'info' in info:
            info = info['info']

        return real_wrapper(func.__name__, info)

    USER_FUNCS_BY_NAME[wrapper.__name__] = (wrapper, func)

    return wrapper


def add_tool_deps(pkg, data):
    def iter_tools():
        for k, v in simple_funcs():
            kk = '$(' + k.upper() + '_'

            if kk in data:
                cc = deep_copy(pkg['constraint'])
                cc['host'] = cc['target']

                yield v(cc)

    return []
    return list(iter_tools())


def gen_packs(host=current_host_platform(), targets=['x86_64', 'aarch64']):
    for name, func in simple_funcs():
        for target in targets:
            yield func({'target': target, 'host': host})


def load_plugins(where):
    def iter_plugins():
        for x in sorted(os.listdir(where)):
            if '~' not in x and '#' not in x:
                yield where + '/' + x

    for x in iter_plugins():
        with open(x, 'r') as f:
            data = '__file__ = "' + x + '"; __name__ = "' + os.path.basename(x) + '"\n\n' + f.read()

            exec data in globals()
