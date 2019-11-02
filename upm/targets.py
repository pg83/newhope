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
def gen_fetch_node_3(url, name, deps=[]):
    fname = y.calc_pkg_full_name(url)

    res = y.fix_v2({
        'node': {
            'kind': 'fetch',
            'name': name,
            'url': url,
            'pkg_full_name': fname,
            'build': [
                'source fetch_url $(URL_BASE) $(URL) $IDIR',
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


@y.cached()
def gen_fetch_node_2(url, dep, curl):
    fname = os.path.basename(url)
    codec = y.calc_mode(fname)

    res = {
        'node': {
            'kind': 'fetch_2',
            'name': 'fetch_url_2',
            'build': [
                'cd $IDIR && {curl} -L -k -o "{url}" "{fname}"'.format(curl=curl, url=url, fname=fname),
            ],
            'prepare': [],
            'codec': 'tr',
        },
        'deps': [dep],
    }

    return y.store_node_plain(res)


@y.cached()
def gen_unpack_node(pkg):
    mpkg = y.mgr_pkg_mark(pkg)

    return {
        'inputs': [pkg, y.build_scripts_path()],
        'output': mpkg,
        'build': [
            'export PATH={path}'.format(path=y.build_scripts_dir()),
            'source set_env',
            'source rmmkcd ' + os.path.dirname(mpkg),
            y.prepare_untar_for_mf(pkg),
            'echo 42 > ' + mpkg,
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
