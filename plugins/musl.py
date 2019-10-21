def musl0(info, codec, deps):
    return system00(info)

    return {
        'code': """
            ./configure --prefix=$(INSTALL_DIR) --enable-static --disable-shared || exit 1
            make && make install
        """,
        'src': 'https://www.musl-libc.org/releases/musl-1.1.24.tar.gz',
        'deps': deps,
    }


@y.options()
def musl2(info):
    return musl0(info, 'gz', [make2_run(info), bestbox2_run(info)])


@y.options()
def musl1(info):
    return musl0(info, 'xz', [make2_run(info), bestbox2_run(info), tar2_run(info), xz2_run(info)])


@y.options()
def musl(info):
    return musl0(info, 'xz', [make1_run(info), bestbox1_run(info), tar1_run(info), xz1_run(info), curl1_run(info)])
