@y.ygenerator(tier=0, kind=['box'])
def sed0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/sed/sed-4.7.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '4.7',
        'meta': {
            'depends': ['iconv', 'intl'],
        }
    }
