@y.ygenerator(tier=2)
def bash0():
    def do():
        yield '--disable-extended-glob-default'
        yield '--enable-extended-glob'
        yield '--enable-job-control'

    return {
        'code': """
            export CFLAGS="-fpermissive $CFLAGS -w"
            source fetch "https://ftp.gnu.org/gnu/bash/bash-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --without-bash-malloc --disable-nls  {extra}
            $YMAKE
            $YMAKE install
        """.replace('{extra}', ' '.join(do())),
        'version': '5.0',
        'meta': {
            'kind': ['tool'],
            'depends': ['readline', 'ncurses', 'intl', 'iconv']
        }
    }

