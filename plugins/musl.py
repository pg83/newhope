def musl0(codec, deps):
    return {
        'code': """
            #pragma cc

            export LDFLAGS=--static
            export CFLAGS=-O2
            export CROSS_COMPILE=$TOOL_CROSS_PREFIX

            ./configure --prefix=$(INSTALL_DIR) --enable-static --disable-shared && make && make install
        """,
        'src': 'https://www.musl-libc.org/releases/musl-1.1.23.tar.gz',
        'deps': deps,
    }


@helper
def musl2(info):
    return musl0('gz', [make2(info), bestbox2(info)])


@helper
def musl1(info):
    return musl0('xz', [make2(info), bestbox2(info), tar2(info), xz2(info)])


@helper
def musl(info):
    return musl0('xz', [make1(info), bestbox1(info), tar1(info), xz1(info), curl1(info)])
