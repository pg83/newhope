@y.package
def wget0():
    return {
        'code': '''
             source fetch "https://ftp.gnu.org/gnu/wget/wget-{version}.tar.gz" 1
             export CFLAGS="-Dhas_key=wget_has_key $OPENSSL_INCLUDES $METALINK_CFLAGS $PCRE2_CFLAGS $CFLAGS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared --with-ssl=openssl || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
             ($YUPX $IDIR/bin/*) || true
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['openssl', 'libmetalink', 'iconv', 'intl', 'libunistring', 'pcre', 'zlib', 'make', 'c', 'upx'],
        }
    }
