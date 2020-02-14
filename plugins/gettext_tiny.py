@y.package
def gettext_tiny0():
    return {
        'code': """
            source fetch "https://github.com/sabotage-linux/gettext-tiny/archive/{version}.zip" 0
            cd gettext*
            $YMAKE -j $NTHRS AR="$AR" RANLIB="$RANLIB" CC="$CC" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS $LIBS" LIBINTL="MUSL" all || exit 1
            $YMAKE LIBINTL="MUSL" DESTDIR="$IDIR" prefix=/ install
        """,
        'version': '55a2119d06403e05808d89eedc9e94a20e87cbd3',
        'meta': {
            'kind': ['library', 'tool'],
            'depends': ['iconv', 'make', 'c'],
            'provides': [
                {'lib': 'intl', 'configure': {'opt': '--with-libintl-prefix={pkgroot}'}},
            ],
        },
    }
