@y.package
def glib0():
    return {
        'code': """
             source fetch "http://ftp.acc.umu.se/pub/gnome/sources/glib/2.30/glib-{version}.tar.xz" 1
             export CFLAGS="-D_GNU_SOURCE=1 -I$(pwd)/inc $CFLAGS"
             (mkdir inc && cd inc && mkdir sys && cd sys && echo '#include <sys/sysmacros.h>' > mkdev.h)
             FFI_INC=$(echo "$CFLAGS" | tr ' ' '\n' | grep ffi | grep include)
             export CFLAGS="$FFI_INC $CFLAGS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-libiconv=gnu --disable-nls || exit 1
             echo '#!'$YSHELL > tmp && cat libtool >> tmp && mv tmp libtool && chmod +x libtool
             $YMAKE -j $NTHRS || exit 1
             $YMAKE install
        """,
        'version': '2.30.3',
        'meta': {
            'kind': ['library'],
            'depends': ['iconv', 'intl', 'libffi', 'pkg-config-int', 'coreutils', 'python', 'zlib', 'dash', 'pcre2'],
            'provides': [
                {
                    'lib': 'glib-2.0', 
                    'extra': [
                        {'libs': '-framework CoreServices -framework CoreFoundation'},
                        {'ipath': '{pkgroot}/include/glib-2.0'},
                        {'ipath': '{pkgroot}/lib/glib-2.0/include'},
                    ],
                },
            ],
        },
    }
