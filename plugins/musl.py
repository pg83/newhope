def musl0(info, codec, deps):
    return {
        'code': """
            ./configure --prefix=$(INSTALL_DIR) --enable-static --disable-shared || exit 1
            make && make install
        """,
        'src': 'https://www.musl-libc.org/releases/musl-1.1.24.tar.gz',
        'deps': deps,
    }


@y.helper
def musl2(info):
    return musl0(info, 'gz', [make2(info), bestbox2(info)])


@y.helper
def musl1(info):
    return musl0(info, 'xz', [make2(info), bestbox2(info), tar2(info), xz2(info)])


@y.helper
def musl(info):
    return musl0(info, 'xz', [make1(info), bestbox1(info), tar1(info), xz1(info), curl1(info)])
