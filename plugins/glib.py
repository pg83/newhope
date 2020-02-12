@y.package
def glib0():
    if '{os}' == 'darwin':
        extra = [
            {'env': 'GLIB_LIBS', 'value': '"-framework CoreServices -framework CoreFoundation"'},
        ]
    else:
        extra = []

    return {
        'code': """
             source fetch "http://ftp.acc.umu.se/pub/gnome/sources/glib/2.30/glib-{version}.tar.xz" 1
             export CFLAGS="-D_GNU_SOURCE=1 -I$(pwd)/inc $CFLAGS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-libiconv=gnu --disable-nls || exit 1
             echo '#!'$YSHELL > tmp && cat libtool >> tmp && mv tmp libtool && chmod +x libtool
             $YMAKE -j $NTHRS || exit 1
             $YMAKE install
        """,
        'version': '2.30.3',
        'meta': {
            'kind': ['library'],
            'depends': ['iconv', 'intl', 'libffi', 'pkg-config-int', 'coreutils', 'python', 'zlib', 'dash', 'pcre'],
            'provides': [
                {'lib': 'glib-2.0'},
                {'env': 'GLIB_CFLAGS', 'value': '"-I{pkgroot}/include/glib-2.0 -I{pkgroot}/lib/glib-2.0/include"'},
                {'env': 'CPPFLAGS', 'value': '"-I{pkgroot}/include/glib-2.0 -I{pkgroot}/lib/glib-2.0/include $CPPFLAGS"'},
            ] + extra,
        },
    }
