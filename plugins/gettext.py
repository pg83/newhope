@ygenerator(tier=1, kind=['core', 'dev', 'library', 'tool'], cached=['deps', 'num', 'info'])
def gettext0(deps, num, info):
    func1 = find_build_func('libiconv', num=num - 1)

    if num > 4:
        func2 = find_build_func('ncurses', num=num - 1)
    else:
        func2 = find_build_func('ncurses', num=num)

    extra = []

    extra.append('--with-libiconv-prefix=$(MNGR_{N}_DIR)'.format(N=func1.__name__.upper()))
    extra.append('--with-libncurses-prefix=$(MNGR_{N}_DIR)'.format(N=func2.__name__.upper()))

    opts = [
        '--with-included-libunistring',
        '--with-included-libxml',
        '--with-included-gettext',
    ]

    return {
        'src': 'https://ftp.gnu.org/gnu/gettext/gettext-0.20.1.tar.gz',
        'code': """
            ./configure --prefix=$IDIR --enable-static --disable-shared {opts} {extra} || exit 1
            $YMAKE -j2 || exit 1
            $YMAKE install
        """.format(extra=' '.join(extra), opts=' '.join(opts)),
        'prepare': '$(ADD_PATH)',
        'deps': [func2(info)] + deps,
        'version': '0.20.1',
    }
