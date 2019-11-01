@ygenerator(tier=1, kind=['core', 'dev', 'library', 'tool'], cached=['deps', 'num', 'info'])
def gettext0(deps, num, info):
    extra = []

    if num > 3:
        extra.append('--with-libiconv-prefix=$(MNGR_{N}_DIR)'.format(N='DEVTOOLS' + str(num - 1)))
        extra.append('--with-libncurses-prefix=$(MNGR_{N}_DIR)'.format(N='DEVTOOLS' + str(num - 1)))

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
        'deps': deps,
        'version': '0.20.1',
    }
