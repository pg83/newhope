@helper
def busybox(info):
    cc = info['info']
    gen_func = info['generator_func']

    ver = '1.30.1'

    return {
        'code': """
            #pragma cc

            make CROSS_COMPILE=$TOOL_CROSS_PREFIX defconfig
            make CROSS_COMPILE=$TOOL_CROSS_PREFIX
            (./busybox >& $(INSTALL_DIR)/check_cross) || true
            mkdir $(INSTALL_DIR)/original && mv ./busybox $(INSTALL_DIR)/original/
        """,
        'src': 'https://www.busybox.net/downloads/busybox-' + ver + '.tar.bz2',
        'version': ver,
        'deps': [gen_func('bestbox1')(cc), gen_func('make2')(cc)],
    }


@helper
def busybox1(info):
    host = info['info']['host']
    arch = {'aarch64': 'arm81'}.get(host, host)
    ver = '1.31.0'

    return {
        'code': 'mkdir -p $(INSTALL_DIR)/bin && cd $(INSTALL_DIR)/bin && $(FETCH_URL_FILE) && mv busybox* busybox && chmod +x busybox',
        'src': 'https://www.busybox.net/downloads/binaries/' + ver + '-defconfig-multiarch-musl/busybox-' + arch,
        'version': ver,
    }
