@ygenerator(tier=0, kind=['core', 'dev', 'tool'], cached=['info', 'deps', 'codec', 'num'])
def curl0(info, deps, codec, num):
    func = find_build_func('mbedtls', num=num - 1)

    return {
        'code': """
            ./configure --prefix=$IDIR --with-mbedtls=$(MNGR_$(SS)_DIR) --enable-static --disable-shared
            $YMAKE -j2
            $YMAKE install
        """.replace('$(SS)', func.__name__.upper()),
        'src': 'https://curl.haxx.se/snapshots/curl-7.67.0-20191011.tar.bz2',
        'deps': [func(info)] + deps,
        'codec': codec,
        'version': '7.67.0',
    }
