import sys
import imp
import importlib
import functools
import itertools

from upm_iface import y


MY_FUNCS = {}


def fix_v2(v):
    assert v is not None

    try:
        v['node']
    except Exception:
        v = y.restore_node_simple(v)

    v = y.deep_copy(v)
    n = v['node']

    if 'codec' not in n:
        n['codec'] = 'xz'

    if 'url' in n:
        if 'pkg_full_name' not in n:
            n['pkg_full_name'] = y.calc_pkg_full_name(n['url'])

    return v


@y.cached()
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


def options(folders=REPACK_FUNCS, convert_to_v2=True, store_out=True, use_cache=True):
    return modifier(folders=folders, convert_to_v2=convert_to_v2, store_out=store_out, use_cache=use_cache)


def deco_fix_info():
    @y.wraps(set_name=deco_fix_info)
    def wrapper(info):
        return y.subst_info(info.get('info', info))

    return wrapper


def deco_run_v1_plugin(func):
    @y.wraps(set_name=deco_run_v1_plugin)
    def wrapper(info):
        return y.v1_to_v2(func, info)

    return wrapper


def deco_id(func):
    @y.wraps(set_name=deco_id)
    def wrappper(info):
        return func(info)

    return wrapper


def deco_fix_v2():
    @y.wraps(set_name=deco_fix_v2)
    def wrapper(info):
        return fix_v2(info)

    return wrapper


def deco_store_node():
    @y.wraps(set_name=deco_store_node)
    def wrapper(info):
        return y.store_node(info)

    return wrapper


def mcalcer1(**kwargs):
    res = y.deep_copy(kwargs)

    def wrapper(func):
        def iter_funcs():
            yield deco_fix_info()

            if res['convert_to_v2']:
                yield deco_run_v1_plugin(func)
            else:
                yield deco_id(func)

            yield deco_fix_v2()

            if res['store_out']:
                yield deco_store_node()

        return y.compose_simple(*reversed(list(iter_funcs())))

    return wrapper


@y.cached()
def mcalcer2(info, res, func_name, folders, dep):
    data = y.restore_node(dep)
    data = folders_calc(data['node'](), folders, func_name, dep, info)

    if res['store_out']:
        data = y.store_node(data)

    return data


def reg_in_funcs(func):
    MY_FUNCS[func.__name__] = func

    return func


def reg_in_plug(func, arg=y.plugins.__dict__):
    arg[func.__name__] = func

    return func


def set_func_name(func, name):
    func.__name__ = name.encode('utf-8')

    return func


def check_not_null(func):
    def wrapper(info):
        res = func(info)

        assert res is not None
        return res

    return wrapper


def reg_main(f, **kwargs):
    def sn(ff):
        return set_func_name(ff, f.__name__)

    return y.compose_simple(sn, use_cache, reg_in_funcs, sn, check_not_null, mcalcer1(**kwargs))


def reg_slave(fn):
    def sn(ff):
        return set_func_name(ff, fn)

    return y.compose_simple(sn, use_cache, reg_in_funcs, reg_in_plug, sn, check_not_null, add_xz_dep, sn)


def flt_deps(deps):
    for x, d in [(y.restore_node_simple(d)['node']['name'], d) for d in deps]:
        if 'xz' in x or 'tar' in x:
            yield d, x


def add_xz_dep(func):
    @y.wraps(set_name=func)
    def wrapper(info):
        res = y.deep_copy(y.restore_node_simple(func(info)))

        #print res['deps'], res['node']['name']

        slave = y.restore_node_simple(res['deps'][0])
        extra = list(flt_deps(slave['deps']))
        res['deps'] = res['deps'] + [e[0] for e in extra]

        #print [(y.restore_node_simple(d)['node']['name'], d) for d in slave['deps']]
        #print res['deps']

        return y.store_node(res)

    return wrapper


def use_cache(func):
    @y.wraps(set_name=func, use_cache=True)
    def wrapper(args):
        return func(args)

    return wrapper


def modifier(**kwargs):
    res = y.deep_copy(kwargs)
    folders = res.pop('folders') or {}

    def gen_other_one(mf, fn, my_folders):
        @reg_slave(fn)
        def folder_func(info):
            return mcalcer2(info, res, fn, my_folders, mf(info))

        return folder_func

    def gen_other(mf):
        for k, fl in folders.items():
            gen_other_one(mf, mf.__name__ + '_' + k, fl)

        return mf

    def wrap_func(func):
        rm = reg_main(func, **res)

        return gen_other(rm(func))

    return wrap_func


def gen_all_funcs():
    for k in sorted(MY_FUNCS.keys()):
        yield MY_FUNCS[k]
