import os
import sys


@y.cached()
def gen_fetch_node(url):
    res = {
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
    }

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


def gen_packs_1(host=None, targets=['x86_64', 'aarch64'], os=['linux', 'darwin']):
    host = host or y.current_host_platform()

    for target in y.iter_targets(host):
        for func in y.gen_all_funcs():
            yield func(y.deep_copy({'host': host, 'target': target}))


def gen_packs(*args, **kwargs):
    for x in gen_packs_1(*args, **kwargs):
        assert x
        yield x
