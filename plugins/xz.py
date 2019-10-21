def xz0(info, deps, codec):
    return {
        'code': './configure --prefix=$(INSTALL_DIR) --disable-shared --enable-static && make && make install',
        'prepare': '$(ADD_PATH)',
        'src': 'https://sourceforge.net/projects/lzmautils/files/xz-5.2.4.tar.gz/download',
        'deps': deps,
        'codec': codec,
    }


@y.options()
def xz2(info):
    return xz0(info, [make2_run(info), bestbox2_run(info), tar2_run(info)], 'gz')


@y.options()
def xz1(info):
    return xz0(info, [make2_run(info), bestbox2_run(info), tar2_run(info), xz2_run(info)], 'xz')


@y.options()
def xz(info):
    return xz0(info, [make1_run(info), bestbox1_run(info), tar1_run(info), xz1_run(info), curl2_run(info)], 'xz')
