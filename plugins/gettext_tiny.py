@y.package
def gettext_tiny0():
    return {
        'code': """
            source fetch "https://github.com/sabotage-linux/gettext-tiny/archive/{version}.zip" 0
            cd gettext*
            $YMAKE -j $NTHRS AR="$AR" RANLIB="$RANLIB" CC="$CC" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS $LIBS" LIBINTL="MUSL" all || exit 1
            $YMAKE LIBINTL="MUSL" DESTDIR="$IDIR" prefix=/ install
        """,
        'meta': {
            'depends': ['iconv', 'make', 'c'],
            'provides': [
                {'lib': 'intl'},
                {'configure': '--with-libintl-prefix={pkgroot}'},
                {'tool': 'XGETTEXT', 'value': '{pkgroot}/bin/xgettext'},
            ],
        },
    }
