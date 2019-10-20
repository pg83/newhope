import sys
import functools

from .ft import deep_copy, singleton, cached
from .db import deref_pointer, store_node, restore_node
from .loader import load_plugins, load_plugins_code
from .user import v1_to_v2
from .ndk import iter_android_ndk_20
from .cc import iter_targets, join_versions
from .helpers import current_host_platform
from .xpath import xp


MY_FUNCS = []


def folders_calc(data, folders, func_name):
    print >>sys.stderr, data, folders, func_name

    def iter_parts():
        yield func_name

        for x in folders:
            yield x[1:]

    rdata = restore_node(data)
    rnode = rdata['node']()
    bad_name = '_'.join(iter_parts())
    version = rnode.get('version')

    res = {
        'node': {
            'build': [
                ('cp -R $(MNGR_%s_DIR)/%s $(INSTALL_DIR)/') % (bad_name.upper(), x[1:]) for x in folders
            ],
            'name': bad_name,
            'kind': 'splitter',
            'codec': 'xz',
            'func_name': func_name,
            'constraint': rnode['constraint'],
        },
        'deps': [data],
    }

    if version:
        res['node']['version'] = version

    return res


def options(folders=None, convert_to_v2=True, helper=True, store_out=True):
    return modifier(folders=folders, decorator='options', convert_to_v2=convert_to_v2, helper=helper, store_out=store_out)


def calcer_key(info, res, func):
    return [info, res, func.__name__]


@cached(key=calcer_key)
def mcalcer(info, res, func):
    if res['helper']:
        info = info.get('info', info)

    if res['convert_to_v2']:
        data = v1_to_v2(func, info)
    else:
        data = func(info)

    if res['folders']:
        data = folders_calc(data, res['folders'], func.__name__)

    if res['store_out']:
        data = store_node(data)

    return data


def modifier(**kwargs):
    res = deep_copy(kwargs)

    def wrap_func(func):
        @functools.wraps(func)
        def wrapper(info):
            return mcalcer(info, res, func)

        MY_FUNCS.append(wrapper)

        return wrapper

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
        if x:
            yield x


class IFace(object):
    pass


y = IFace()


y.helper = options()
y.load_plugins = load_plugins
y.gen_all_funcs = gen_all_funcs
y.store_node = store_node
y.restore_node = restore_node
y.singleton = singleton
y.cached = cached
y.gen_packs = gen_packs
y.current_host_platform = current_host_platform
y.splitter = options
y.join_versions = join_versions
y.xp = xp
