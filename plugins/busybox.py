

/*
@y.options(repacks=None)
def busybox_run(info):
    if y.xp('/info/info/host/os') == 'darwin':
        return system00(info)

    ver = '1.30.1'

    return y.to_v2({
        'code': """
            make CROSS_COMPILE=$TOOL_CROSS_PREFIX defconfig
            make CROSS_COMPILE=$TOOL_CROSS_PREFIX
            (./busybox >& $(INSTALL_DIR)/check_cross) || true
            mkdir $(INSTALL_DIR)/bin && mv ./busybox $(INSTALL_DIR)/bin/
        """,
        'src': 'https://www.busybox.net/downloads/busybox-' + ver + '.tar.bz2',
        'version': ver,
        'deps': [bestbox1_run(info), make1_run(info), tar1_run(info), xz1_run(info), curl1_run(info)],
    }, info)
*/

@y.cached()
def busybox0(info, deps, codec):
    if y.xp('/info/info/host/os') == 'darwin':
        return system00(info)

    host = info['info']['host']['arch']
    arch = {'aarch64': 'arm81'}.get(host, host)
    ver = '1.31.0'

    return y.to_v2({
        'code': """
            mkdir -p $(INSTALL_DIR)/bin
            cd $(INSTALL_DIR)/bin
            $(FETCH_URL_FILE)
            mv busybox-* busybox
            chmod +x busybox
        """,
        'src': 'https://www.busybox.net/downloads/binaries/' + ver + '-defconfig-multiarch-musl/busybox-' + arch,
        'version': ver,
        'deps': deps,
        'codec': codec,
    }, info)


y.register_func_generator({
    'support': ['linux'],
    'tier': -1,
    'kind': ['core', 'dev', 'tool'],
    'template': """
@y.options({options})
def {name}{num}(info):
    return busybox0(info, {deps}, "{codec}")
"""
})
