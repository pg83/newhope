@y.ygenerator()
def bash0():
    def do():
        yield '--disable-extended-glob-default'
        yield '--enable-extended-glob'
        yield '--enable-job-control'

    return {
        'code': """
            export CFLAGS="-fpermissive $CFLAGS -w"
            export LIBS="$LDFLAGS $LIBS"
            source fetch "https://ftp.gnu.org/gnu/bash/bash-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --without-bash-malloc --disable-nls  {extra}
            $YMAKE -j $NTHRS
            $YMAKE install
        """.replace('{extra}', ' '.join(do())),
        'version': '5.0',
        'meta': {
            'kind': ['tool'],
            'depends': ['readline', 'ncurses', 'intl', 'iconv']
        }
    }
