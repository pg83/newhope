import os
import sys


@y.cached()
def gen_fetch_node(url):
    res = y.fix_v2({
        'node': {
            'kind': 'fetch',
            'name': 'fetch_url',
            'url': url,
            'pkg_full_name': y.calc_pkg_full_name(url),
            'build': [
                'source fetch_url $(URL_BASE) $(URL) $IDIR',
            ],
            'codec': 'tr',
        },
        'deps': [],
    })

    return y.store_node_plain(res)


@y.cached()
def gen_fetch_node_3(url, name, deps, v):
    fname = y.calc_pkg_full_name(url)

    res = y.fix_v2({
        'node': {
            'kind': 'fetch',
            'name': name,
            'url': url,
            'pkg_full_name': fname,
            'build': [
                'source fetch_url {ub} {u} $IDIR'.format(ub=fname, u=url),
            ],
            'prepare' : [
                'ln $(CUR_DIR)/{fname} $BDIR/runtime/'.format(fname=fname)
            ],
            'codec': 'tr',
        },
        'deps': deps,
    })

    res['node']['file'] = '$BDIR/runtime/' + fname

    return y.store_node_plain(res)


def gen_unpack_node(pkg):
    mpkg = y.mgr_pkg_mark(pkg)
    vis_name = pkg[4:]

    return {
        'inputs': [pkg, y.build_scripts_path()],
        'output': mpkg,
        'build': [
            '. "{path}/build" && source unpackage {codec} "{vis_name}"'.format(path=y.build_scripts_dir(), vis_name=vis_name, codec=y.calc_mode(vis_name))
        ],
    }


def gen_packs_1(constraints=None):
    constraints = constraints or y.get_all_constraints

    for c in constraints():
        for func in y.gen_all_funcs():
            yield func(y.deep_copy(c))

        #for t in y.find_compiler_x(y.deep_copy(c)):
            #yield t


def gen_packs(*args, **kwargs):
    for x in gen_packs_1(*args, **kwargs):
        assert x
        yield x
