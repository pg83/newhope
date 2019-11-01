@ygenerator(tier=-1, kind=['core', 'dev', 'tool'], cached=['deps', 'num'])
def bash0(deps, num):
    extra = [
        '--with-included-gettext',
        '--disable-extended-glob',
        '--disable-extended-glob-default',
        #'--enable-readline',
    ]

    if num > 4:
        extra.append('--with-curses=$(MNGR_{N}_DIR)'.format(N='DEVTOOLS' + str(num - 1)))

    return {
            'code': """
            ./configure --prefix=$IDIR --without-bash-malloc --disable-nls  {extra} --enable-minimal-config
            $YMAKE
            $YMAKE install
""".format(extra=' '.join(extra)),
        'src': 'https://ftp.gnu.org/gnu/bash/bash-5.0.tar.gz',
        'prepare': '$(ADD_PATH)',
        'deps': deps,
        'version': '5.0'
    }
