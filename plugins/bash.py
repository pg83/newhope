@y.package
def bash0():
    def do():
        yield '--disable-extended-glob-default'
        yield '--enable-extended-glob'
        yield '--enable-job-control'

    return {
        'code': """
            export CFLAGS="-fpermissive $CFLAGS -w"
            export LIBS="$LDFLAGS $LIBS"
            export CFLAGS="$CFLAGS $LIBS"
            source fetch "https://ftp.gnu.org/gnu/bash/bash-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --without-bash-malloc --disable-nls  {extra}
            $YMAKE LIBS_FOR_BUILD="$LIBS" -j $NTHRS
            $YMAKE install
        """.replace('{extra}', ' '.join(do())),
        'meta': {
            'kind': ['tool'],
            'depends': ['ncurses', 'intl', 'iconv', 'make', 'c'],
            'provides': [
                {'tool': 'YBASH', 'value': '{pkgroot}/bin/bash'},
            ],
        }
    }
