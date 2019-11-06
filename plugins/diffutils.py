@ygenerator(tier=2, kind=['core', 'box', 'tool'])
def diffutils0():
    version = '3.7'

    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/diffutils/diffutils-{version}.tar.xz" 1
             $YSHELL ./configure --prefix=$IDIR --disable-gcc-warnings || exit 1
             $YMAKE -j2
             $YMAKE install
        """.format(version=version),
        'version': version,
        'meta': {
            'depends': ['iconv', 'intl', 'libsigsegv']
        },
    }
