import os
import imp
import sys
import platform
import json
import base64
import functools
import itertools

from .ft import singleton, cached, fp, deep_copy
from .cc import find_compiler, is_cross, iter_targets
from .gen_id import to_visible_name, calc_pkg_full_name
from .xpath import xp
from .db import restore_node, store_node, pointer, intern_struct
from .subst import subst_kv_base


def join_versions(deps):
    def iter_v():
        for d in deps:
            yield xp('/d/node/version')

    return '-'.join(iter_v())


@singleton
def current_host_platform():
    return {
        'arch': platform.machine(),
        'os': platform.system().lower()
    }


@cached(key=lambda x: x)
def find_compiler_id(info):
    for x in find_compiler(info):
        return x

    raise Exception('shit happen %s' % info)


@cached(key=lambda x: x)
def find_compilers(info):
    def iter_compilers():
        if is_cross(info):
            cinfo = deep_copy(info)
            cinfo['target'] = cinfo['host']

            yield find_compiler_id(cinfo)

        yield find_compiler_id(info)

    return list(iter_compilers())


def subst_info(info):
    info = deep_copy(info)

    if 'host' not in info:
        info['host'] = current_host_platform()

    if 'target' not in info:
        info['target'] = deep_copy(info['host'])

    return info


USER_FUNCS_BY_NAME = {}


def simple_funcs():
    for k in sorted(USER_FUNCS_BY_NAME.keys()):
        yield k, USER_FUNCS_BY_NAME[k][0]


def to_lines(text):
    def iter_l():
        for l in text.split('\n'):
            l = l.strip()

            if l:
                yield l

    return list(iter_l())


@cached(key=lambda x: x)
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

    try:
        data = full_data['code']
    except TypeError:
        return full_data

    if '#pragma cc' not in data:
        if './configure' not in data:
            compilers = []

    node = {
        'name': func.__name__,
        "constraint": info,
        "from": func.__name__ + '.py',
    }

    def iter_prepare():
        for l in to_lines(full_data.get('prepare', '')):
            yield l

    node['prepare'] = list(iter_prepare())
    node['codec'] = 'xz'

    for x in ('version', 'codec'):
        if x in full_data:
            node[x] = full_data[x]

    for k in ('src', 'url'):
        if k in full_data:
            node['url'] = full_data[k]
            node['pkg_full_name'] = calc_pkg_full_name(node['url'])

    def iter_extra_lines():
        if '$(FETCH_URL' not in data and 'url' in node:
            yield '$(FETCH_URL)'

    if 'subst' in full_data:
        data = subst_kv_base(data, full_data['subst'])

    node['build'] = list(iter_extra_lines()) + to_lines(data)

    def iter_deps():
        for x in compilers:
            yield x

        for x in full_data['deps']:
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


def move_many(fr, dirs):
    return '\n'.join([('cp -R %s $(INSTALL_DIR)/' % (fr + x)) for x in dirs]) + '\n'


def splitter(folders=[]):
    def genwrapper(func):
        return real_splitter(helper(func), folders)

    return genwrapper


def x_key(v):
    a, b, c = v

    return (a, b.__name__, c)


@cached(key=x_key)
def real_splitter(func, folders):
    @helper
    def splitter_func(info):
        fi = func(info)
        name = restore_node(fi)['node']()['name']

        def iter_cut():
            yield 'cut'
            yield func.__name__
            yield name

        return {
            'code': '\n'.join([('cp -R $(MNGR_%s_DIR)/%s $(INSTALL_DIR)/') % (name.upper(), x[1:]) for x in folders]),
            'name': '-'.join(iter_cut()),
            'kind': 'splitter',
            'deps': [fi, tar1(info), xz1(info), bestbox1(info)],
        }

    return splitter_func


def gen_packs(host=current_host_platform(), targets=['x86_64', 'aarch64'], os=['linux', 'darwin']):
    if not os:
        os = [host['os']]

    for name, func in simple_funcs():
        for target in iter_targets(host):
            yield func({'host': host, 'target': target})


def load_plugins_code(where):
    def iter_plugins():
        for x in os.listdir(where):
            if '~' not in x and '#' not in x:
                path = where + '/' + x

                with open(path, 'r') as f:
                    yield path, f.read()

    return dict(iter_plugins())


def load_plugins_base(plugins):
    for x in sorted(plugins.keys()):
        data = '__file__ = "' + x + '"; __name__ = "' + os.path.basename(x) + '"\n\n' + plugins[x]

        exec data in globals()


def load_plugins(where):
    builtin_plugins = {}
    ## builtin_plugins
    load_plugins_base(builtin_plugins)

    for x in itertools.chain(where):
        load_plugins_base(load_plugins_code(os.path.abspath(x)))
