import sys
import imp
import importlib
import functools
import itertools

from upm_iface import y
from upm_ft import deep_copy, cached
from upm_db import store_node, restore_node, restore_node_simple
from upm_ndk import iter_android_ndk_20
from upm_cc import iter_targets
from upm_helpers import current_host_platform, subst_info
from upm_gen_id import calc_pkg_full_name


MY_FUNCS = []


def fix_v2(v):
    assert v is not None

    try:
        v['node']
    except Exception:
        v = restore_node_simple(v)

    v = deep_copy(v)
    n = v['node']

    if 'codec' not in n:
        n['codec'] = 'xz'

    if 'url' in n:
        if 'pkg_full_name' not in n:
            n['pkg_full_name'] = calc_pkg_full_name(n['url'])

    return v


@cached()
def folders_calc(node, folders, func_name, dep, info):
    version = node.get('version')
    kind = func_name.split('_')[-1]

    by_kind = {
        'dev': [
            'export CFLAGS="-I$(MNGR_%s_INC_DIR) $CFLAGS"' % func_name.upper(),
            'export LDFLAGS="-L$(MNGR_%s_LIB_DIR) $LDFLAGS"' % func_name.upper(),
        ],
        'run': [
            '$(ADD_PATH)',
        ],
        'doc': [],
        'log': [],
    }

    def iter_ops():
        if kind == 'run':
            yield 'mkdir -p $(INSTALL_DIR)/bin'

            for x in [('cp -R $(MNGR_%s_DIR)/%s/* $(INSTALL_DIR)/bin/ >& /dev/null') % (node['name'].upper(), x[1:]) for x in folders]:
                yield x
        else:
            for y in (('cp -R $(MNGR_%s_DIR)/%s $(INSTALL_DIR)/') % (node['name'].upper(), x[1:]) for x in folders):
                yield y

    res = {
        'node': {
            'build': list(iter_ops()),
            'name': func_name,
            'kind': 'splitter',
            'func_name': func_name,
            'constraint': node['constraint'],
            'codec': node['codec'],
            'prepare': by_kind[kind],
        },
        'deps': [dep],
    }

    if version:
        res['node']['version'] = version

    return res


REPACK_FUNCS = {
    'dev': ['/lib', '/include'],
    'run': ['/bin', '/sbin'],
    'doc': ['/share'],
    'log': ['/log'],
}


def options(folders=REPACK_FUNCS, convert_to_v2=True, helper=True, store_out=True):
    return modifier(folders=folders, convert_to_v2=convert_to_v2, helper=helper, store_out=store_out)


def calcer_key(info, res, func):
    return [info, res, func.__name__]


@cached(key=calcer_key)
def mcalcer1(info, res, func):
    if res['helper']:
        info = info.get('info', info)

    info = subst_info(info)

    if res['convert_to_v2']:
        data = y.v1_to_v2(func, info)
        assert data
        data = fix_v2(data)
    else:
        data = fix_v2(func(info))

    return store_node(data)


@cached()
def mcalcer2(info, res, func_name, folders, dep):
    data = restore_node(dep)
    data = folders_calc(data['node'](), folders, func_name, dep, info)

    if res['store_out']:
        data = store_node(data)

    return data


def reg_in_funcs(func):
    MY_FUNCS.append(func)

    return func


def reg_in_plug(func):
    y.register_plugin_func(func)

    return func


def set_func_name(func, name):
    func.__name__ = name.encode('utf-8')

    return func


def check_not_null(func):
    @functools.wraps(func)
    def wrapper(info):
        res = func(info)
        assert res is not None
        return res

    return wrapper


def modifier(**kwargs):
    res = deep_copy(kwargs)
    folders = res.pop('folders') or {}

    def gen_other_one(main_func, func_name, my_folders):
        def folder_func(info):
            return mcalcer2(info, res, func_name, my_folders, main_func(info))

        return reg_in_funcs(reg_in_plug(set_func_name(check_not_null(folder_func), func_name)))

    def gen_other(main_func):
        for k, fl in folders.items():
            gen_other_one(main_func, main_func.__name__ + '_' + k, fl)

        return main_func

    def wrap_func(func):
        @functools.wraps(func)
        def main(info):
            return mcalcer1(info, res, func)

        return gen_other(reg_in_funcs(check_not_null(main)))

    return wrap_func


def gen_all_funcs():
    for f in MY_FUNCS:
        yield f


def gen_packs_1(host=current_host_platform(), targets=['x86_64', 'aarch64'], os=['linux', 'darwin']):
    for func in gen_all_funcs():
        for target in iter_targets(host):
            yield func({'host': host, 'target': target})

    for x in iter_android_ndk_20():
        yield x


def gen_packs(*args, **kwargs):
    for x in gen_packs_1(*args, **kwargs):
        assert x
        yield x
