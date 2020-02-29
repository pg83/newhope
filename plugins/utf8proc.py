@y.package
def utf8proc0():
    return {
        'code': '''
            source fetch "https://github.com/JuliaStrings/utf8proc/archive/v2.4.0.tar.gz" 0
            (mv utf8* xxx && mv xxx/* .)
            ($YMAKE CC="$CC" CFLAGS="$CFLAGS" -j $NTHRS) || true
            touch libutf8proc.so.2.3.1 libutf8proc.so.2 libutf8proc.so
            ($YMAKE CC="$CC" CFLAGS="$CFLAGS" -j $NTHRS)
            $YMAKE prefix=$IDIR install
            (cd $IDIR/lib && rm *so*)
        ''',
        'meta': {
            'kind': ['library'],
            'depends': ['make', 'c'],
            'provides': [
                {'lib': 'utf8proc'},
                {'env': 'UTF8PROC_ROOT', 'value': '{pkgroot}'},
            ]
        }
    }
