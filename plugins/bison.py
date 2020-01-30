@y.package
def bison0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/bison/bison-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --enable-relocatable || exit 1
             $YMAKE -j $NTHRS || true
             $YMAKE || true
             $YMAKE
             $YMAKE install
        """,
        'version': '3.4.2',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['c++', 'm4', 'iconv', 'intl', 'xz', 'perl5']
        },
    }

