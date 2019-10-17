@helper
def busybox(info):
    if xp('/info/info/host/os') == 'darwin':
        return system0(info)

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
        'deps': [bestbox1(info), make1(info), tar1(info), xz1(info), curl1(info)],
    }


@helper
def busybox1(info):
    return busybox0(info, [busybox2(info)], 'gz')


@helper
def busybox2(info):
    return busybox0(info, [system0(info)], 'gz')


def busybox0(info, deps, codec):
    if xp('/info/info/host/os') == 'darwin':
        return system0(info)

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
