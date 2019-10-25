from upm_iface import y


@y.cached()
def gen_fetch_node(url):
    res = {
        'node': {
            'kind': 'fetch',
            'name': 'fetch_url',
            'url': url,
            'pkg_full_name': y.calc_pkg_full_name(url),
            'build': [
                'cd $(INSTALL_DIR) && ((wget -O $(URL_BASE) $(URL) >& $(INSTALL_DIR/log/wget.log)) || (curl -L -k -o $(URL_BASE) $(URL) >&$(INSTALL_DIR/log/curl.log)) && ls -la',
            ],
            'prepare': [
                'mkdir -p $(BUILD_DIR)/fetched_urls/',
                'ln $(CUR_DIR)/$(URL_BASE) $(BUILD_DIR)/fetched_urls/',
            ],
            'codec': 'tr',
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
