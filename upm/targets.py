from upm_iface import y


def gen_packs_1(host=None, targets=['x86_64', 'aarch64'], os=['linux', 'darwin']):
    host = host or y.current_host_platform()

    for func in y.gen_all_funcs():
        for target in y.iter_targets(host):
            yield func({'host': host, 'target': target})

    for x in y.iter_android_ndk_20():
        yield x


def gen_packs(*args, **kwargs):
    for x in gen_packs_1(*args, **kwargs):
        assert x
        yield x
