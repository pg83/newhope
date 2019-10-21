@y.options(folders=[])
def busybox_run(info):
    if y.xp('/info/info/host/os') == 'darwin':
        return system00(info)

    ver = '1.30.1'

    return {
        'code': """
            make CROSS_COMPILE=$TOOL_CROSS_PREFIX defconfig
            make CROSS_COMPILE=$TOOL_CROSS_PREFIX
            (./busybox >& $(INSTALL_DIR)/check_cross) || true
            mkdir $(INSTALL_DIR)/bin && mv ./busybox $(INSTALL_DIR)/bin/
        """,
        'src': 'https://www.busybox.net/downloads/busybox-' + ver + '.tar.bz2',
        'version': ver,
        'deps': [bestbox1_run(info), make1_run(info), tar1_run(info), xz1_run(info), curl1_run(info)],
    }


@y.options(folders=[])
def busybox1_run(info):
    return busybox0(info, [busybox2_run(info)], 'gz')


@y.options(folders=[])
def busybox2_run(info):
    return busybox0(info, [system0(info)], 'gz')


def busybox0(info, deps, codec):
    if 0:
        if xp('/info/info/host/os') == 'darwin':
            return system00(info)

    host = info['info']['host']['arch']
    arch = {'aarch64': 'arm81'}.get(host, host)
    ver = '1.31.0'

    return {
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
    }
