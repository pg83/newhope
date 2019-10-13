@helper
def busybox():
    return {
        'code': """
            #pragma cc

            make CROSS_COMPILE=$TOOL_CROSS_PREFIX defconfig
            make CROSS_COMPILE=$TOOL_CROSS_PREFIX
            (./busybox >& $(INSTALL_DIR)/check_cross) || true
            mkdir $(INSTALL_DIR)/original && mv ./busybox $(INSTALL_DIR)/original/
        """,
        'src': 'https://www.busybox.net/downloads/busybox-1.30.1.tar.bz2',
    }


@helper
def busybox1(info):
    host = info['info']['host']
    arch = {'aarch64': 'arm81'}.get(host, host)

    return {
        'code': 'mkdir $(INSTALL_DIR)/original && cd $(INSTALL_DIR)/original && $(FETCH_URL_FILE) && mv busybox* busybox && chmod +x busybox',
        'src': 'https://www.busybox.net/downloads/binaries/1.31.0-defconfig-multiarch-musl/busybox-' + arch,
    }
