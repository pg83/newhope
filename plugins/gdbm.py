@y.package
def gdbm0():
    return {
        'code': """
             source fetch "ftp://ftp.gnu.org/gnu/gdbm/gdbm-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'kind': ['library'],
            'depends': ['make', 'c'],
            'provides': [
                {'lib': 'gdbm'},
            ],
        },
    }
