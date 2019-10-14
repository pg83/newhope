def xz0(info, deps, codec):
    return {
        'code': './configure --prefix=$(INSTALL_DIR) --disable-shared --enable-static && make && make install',
        'src': 'https://downloads.sourceforge.net/project/lzmautils/xz-5.2.4.tar.gz',
        'deps': deps,
        'codec': codec,
    }


@helper
def xz2(info):
    return xz0(info, [make2(info), bestbox2(info), tar2(info)], 'gz')


@helper
def xz1(info):
    return xz0(info, [make2(info), bestbox2(info), tar2(info), xz2(info), musl2(info)], 'xz')


@helper
def xz(info):
    return xz0(info, [make1(info), bestbox1(info), tar1(info), xz1(info), curl1(info), musl1(info)], 'xz')
