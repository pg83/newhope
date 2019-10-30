@y.cached()
def musl0(info, codec, deps):
    return y.to_v2({
        'code': """
            ./configure --prefix=$(INSTALL_DIR) --enable-static --disable-shared || exit 1
            make -j2 && make install
        """,
        'src': 'https://www.musl-libc.org/releases/musl-1.1.24.tar.gz',
        'deps': deps,
    }, info)


y.register_func_generator({
    'support': ['linux'],
    'tier': 0,
    'kind': ['core', 'dev', 'library'],
    'template': """
@y.options({options})
def {name}{num}(info):
    return musl0(info, "{codec}", {deps})
"""
})
