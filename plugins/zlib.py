def zlib0(info, deps):
    return {
        'src': 'http://zlib.net/zlib-1.2.11.tar.gz',
        'code': """
            which tar; which curl; which xz; which make; ./configure --disable-shared || exit 1
            make && make install
        """,
        'prepare': '$(ADD_PATH)',
        'deps': deps
    }


@helper
def zlib2(info):
    return zlib0(info, devtools_last(info))
