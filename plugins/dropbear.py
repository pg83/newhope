@y.package
def dropbear0():
    return {
        'code': '''
             source fetch "https://matt.ucc.asn.au/dropbear/releases/dropbear-{version}.tar.bz2" 1
             $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared --disable-harden --disable-bundled-libtom || exit 1
             $YMAKE -j $THRS
             $YMAKE install
        ''',
        'version': '2019.78',
        'meta': {
            'kind': ['tool'],
            'depends': ['libtommath', 'libtomcrypt', 'zlib', 'make', 'c']
        }
    }
