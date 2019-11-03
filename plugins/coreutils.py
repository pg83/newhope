@ygenerator(tier=0, kind=['core', 'dev', 'tool'])
def coreutils0(info, num):
    version = '8.31'

    if num < 4:
        func = find_build_func('libiconv', num=num)
    else:
        func = find_build_func('libiconv', num=num - 1)

    return {
        'code': """
             ./configure --prefix=$IDIR --without-gmp --with-libiconv-prefix=$(MNGR_{libname}_DIR) || exit 1
             $YMAKE -j2
             $YMAKE install
        """.format(libname=func.__name__.upper()),
        'url': 'https://ftp.gnu.org/gnu/coreutils/coreutils-' + version + '.tar.xz',
        'extra_deps': [func(info)],
        'version': version,
        'prepare': '$(ADD_PATH)',
    }
