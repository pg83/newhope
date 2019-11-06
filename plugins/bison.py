@ygenerator(tier=2, kind=['core', 'box', 'tool'])
def bison0():
    version = '3.4.2'

    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/bison/bison-{version}.tar.xz" 1
             $YSHELL ./configure --prefix=$IDIR --disable-shared --enable-static --enable-relocatable || exit 1
             $YMAKE -j2
             $YMAKE install
        """.format(version=version),
        'version': version,
        'meta': {
            'depends': ['m4', 'iconv', 'intl']
        },
    }
