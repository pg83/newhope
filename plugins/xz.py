def xz0(info, deps, codec):
    return {
        'code': './configure --prefix=$(INSTALL_DIR) --disable-shared --enable-static && make && make install',
        'prepare': '$(ADD_PATH)',
        'src': 'https://sourceforge.net/projects/lzmautils/files/xz-5.2.4.tar.gz/download',
        'deps': deps,
        'codec': codec,
    }


@y.helper
def xz2(info):
    return xz0(info, [make2(info), bestbox2(info), tar2(info)], 'gz')


@y.helper
def xz1(info):
    return xz0(info, [make2(info), bestbox2(info), tar2(info), xz2(info), musl2(info)], 'xz')


@y.helper
def xz(info):
    return xz0(info, [make1(info), bestbox1(info), tar1(info), xz1(info), curl2(info), musl1(info)], 'xz')


@y.splitter(folders=['/bin'])
def xz_runtime(info):
    return xz(info)
