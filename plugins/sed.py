@ygenerator(tier=0, kind=['core', 'tool', 'box'])
def sed0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/sed/sed-4.7.tar.xz" 1
             $YSHELL ./configure --prefix=$IDIR || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '4.7',
        'meta': {
            'depends': ['iconv', 'intl'],
        }
    }
