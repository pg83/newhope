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
                'source fetch_url "$(URL_BASE)" "$(URL)" "$IDIR"',
            ],
            'codec': 'tr',
        },
        'deps': [],
    })

    return y.store_node_plain(res)


def gen_fetch_node_3(url, name, deps):
    fname = y.calc_pkg_full_name(url)

    res = y.fix_v2({
        'node': {
            'kind': 'fetch',
            'name': name,
            'url': url,
            'pkg_full_name': fname,
            'build': [
                'source fetch_url "{ub}" "{u}" "$IDIR"'.format(ub=fname, u=url),
            ],
            'prepare' : [
                'ln "$(CUR_DIR)/{fname}" "$BDIR/runtime/"'.format(fname=fname)
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
        'inputs': [y.build_scripts_path(), pkg],
        'output': mpkg,
        'build': [
            '. "$2" && source unpackage $(basename "$3")'
        ],
    }


async def gen_packs_1(constraints=None):
    constraints = constraints or y.get_all_constraints

    def iter():
        for c in constraints():
            for func in y.gen_all_funcs():
                yield func(y.deep_copy(c))

    return list(iter())


async def gen_packs(*args, **kwargs):
    return [x for x in await gen_packs_1(*args, **kwargs)]
