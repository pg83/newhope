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
            source fetch "https://ftp.gnu.org/gnu/bash/bash-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --without-bash-malloc --disable-nls  {extra}
            $YMAKE LIBS_FOR_BUILD="$LIBS" -j $NTHRS
            $YMAKE install

            echo 'ln -lf {pkgroot}/bin/bash /etc/alt/sh' > $IDIR/install && chmod +x $IDIR/install
        """.replace('{extra}', ' '.join(do())),
        'version': '5.0',
        'meta': {
            'kind': ['tool'],
            'depends': ['readline', 'ncurses', 'intl', 'iconv', 'make', 'c']
        }
    }
