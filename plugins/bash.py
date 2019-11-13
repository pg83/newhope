@y.ygenerator(tier=2, kind=['core', 'box', 'tool'])
def bash0():
    def do():
        yield '--with-installed-readline'
        yield '--disable-extended-glob'
        yield '--disable-extended-glob-default'
        yield '--enable-minimal-config'
        yield '--enable-job-control'
        yield '--with-curses'

    return {
        'code': """
            export CFLAGS="-fpermissive $CFLAGS -w"
            source fetch "https://ftp.gnu.org/gnu/bash/bash-5.0.tar.gz" 1
            $YSHELL ./configure --prefix=$IDIR --without-bash-malloc --disable-nls  {extra}
            $YMAKE
            $YMAKE install
        """.format(extra=' '.join(do())),
        'version': '5.0',
        'meta': {
            'depends': ['readline', 'ncurses', 'intl', 'iconv']
        }
    }

