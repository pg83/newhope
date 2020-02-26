@y.package
def dropbear0():
    return {
        'code': '''
             source fetch "https://matt.ucc.asn.au/dropbear/releases/dropbear-{version}.tar.bz2" 1
             $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared --disable-harden --disable-bundled-libtom || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['libtommath', 'libtomcrypt', 'zlib', 'make', 'c']
        }
    }
