import os

from upm_iface import y


@y.cached()
def gen_fetch_node(url):
    if 'libarchive.org' in url:
        return gen_fetch_node2(url)

    res = {
        'node': {
            'kind': 'fetch',
            'name': 'fetch_url',
            'url': url,
            'pkg_full_name': y.calc_pkg_full_name(url),
            'build': [
                'source fetch_url $(URL_BASE) $(URL)',
            ],
            'codec': 'tr',
        },
        'deps': [],
    }

    return y.store_node_plain(res)


@y.cached()
def gen_fetch_node2(url):
    res = {
        'node': {
            'kind': 'fetch',
            'name': 'fetch_url',
            'url': url,
            'pkg_full_name': y.calc_pkg_full_name(url),
            'build': [
                'echo $PATH 1>&2',
                '(which curl && which tar && which xz) 1>&2',
                'source fetch_url $(URL_BASE) $(URL)',
            ],
            'codec': 'tr',
        },
        'deps': [],
    }

    return y.store_node_plain(res)


@y.cached()
def gen_unpack_node(pkg):
    mpkg = y.mgr_pkg(pkg)

    res = {
        'node': {
            'name': 'unpack',
            'kind': 'gen_unpack_node',
            'internal': True,
            'inputs': [pkg],
            'output': mpkg,
            'build': [
                y.rmmkcd(os.path.dirname(mpkg)),
                y.prepare_untar_cmd(pkg, '.'),
                'echo 42 > ' + mpkg,
            ],
        },
        'deps': [],
    }

    return y.store_node_plain(res)


def gen_packs_1(host=None, targets=['x86_64', 'aarch64'], os=['linux', 'darwin']):
    host = host or y.current_host_platform()

    for target in y.iter_targets(host):
        for func in y.gen_all_funcs():
            yield func(y.deep_copy({'host': host, 'target': target}))

    for x in y.iter_android_ndk_20():
        yield y.deep_copy(x)


def gen_packs(*args, **kwargs):
    for x in gen_packs_1(*args, **kwargs):
        assert x
        yield x
