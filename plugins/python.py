@y.package
def python0():
    return {
        'code': """
            source fetch "https://www.python.org/ftp/python/{version}/Python-{version}.tar.xz" 1
            export PYTHONHOME=
            $(F_0)
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared --with-signal-module --with-system-expat --with-system-ffi || exit1
            ##echo "#define HAVE_PTH 1" >> pyconfig.h
            ##echo "#undef HAVE_PTHREAD_H" >> pyconfig.h 
            $YMAKE -j $NTHRS || exit 1
            $YMAKE install

            mkdir good && cd good
            $(F_1)
            $(F_2)
            export PYTHONHOME="$IDIR"
            source ./mk_staticpython.sh "$IDIR/bin/python2.7" "2.7" "2" "Py_Main"
        """,
        'extra': [
            {'kind': 'file', 'path': 'Modules/Setup.local', 'data': y.builtin_data('data/Setup.local2')},
            {'kind': 'file', 'path': 'find_modules.py', 'data': y.builtin_data('data/find_modules.py')},
            {'kind': 'file', 'path': 'mk_staticpython.sh', 'data': y.builtin_data('data/mk_staticpython.sh')},
        ],
        'meta': {
            'depends': [
                'ncurses', 'iconv', 'intl', 'zlib', 'pkg-config-int',
                'libffi', 'readline', 'termcap', 'expat', 'sqlite3',
                'make', 'c',
            ],
            'provides': [
                {'lib': 'python2.7'},
                {'tool': 'PYTHON', 'value': '{pkgroot}/bin/staticpython2'},
                {'env': 'PYTHONHOME', 'value': '{pkgroot}/lib/python2.7'},
            ],
            'repacks': {},
        },
    }
