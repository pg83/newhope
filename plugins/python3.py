@y.package
def python30():
    version = '3.8.1'
    ver = '.'.join(version.split('.')[:2])

    return {
        'code': """
            source fetch "https://www.python.org/ftp/python/{version}/Python-{version}.tar.xz" 1
            export PYTHONHOME=
            $(APPLY_EXTRA_PLAN_0)
            $(APPLY_EXTRA_PLAN_1)

            source subst_string Setup OPENSSL_INCLUDE "$OPENSSL_INCLUDES"
            source subst_string Setup LIBFFI_CFLAGS "$LIBFFI_CFLAGS"
            cp Setup Modules/Setup

            $YSHELL ./configure $COFLAGS --prefix=$IDIR --with-system-libmpdec --enable-static --disable-shared --with-signal-module || exit1

            $YMAKE -j $NTHRS || exit 1
            PY=`which ./python.exe || which ./python`
            $PY ./fix.py patch ./setup.py
            DUMP=1 $PY ./setup.py build > data.json
            $PY ./fix.py ./data.json > tmp1
            cat tmp1 > Modules/Setup.local
            $YMAKE -j $NTHRS || exit 1
            $YMAKE -j $NTHRS || exit 1
            $YMAKE install

            cp -R Tools $IDIR/
            mv $IDIR/Tools $IDIR/tools 

            (cd $IDIR/lib/python{ver} && ln -s config-{ver}* config-{ver})
        """.replace('{ver}', ver),
        'version': version,
        'extra': [
            {'kind': 'file', 'path': 'Setup', 'data': y.builtin_data('data/Setup.local')},
            {'kind': 'file', 'path': 'fix.py', 'data': y.builtin_data('data/python3_bc.py')},
            {'kind': 'file', 'path': 'find_modules.py', 'data': y.builtin_data('data/find_modules.py')},
        ],
        'meta': {
            'kind': ['tool'],
            'depends': [
                'ncurses', 'iconv', 'intl', 'zlib',
                'pkg-config', 'libffi', 'readline',
                'termcap', 'mpdecimal', 'xz', 'bzip2',
                'sqlite3', 'openssl', 'dl',
            ],
            'provides': [
                {'lib': 'python3.8'},
                {'env': 'PYTHON3', 'value': '{pkgroot}/bin/python3'},
                {'env': 'PYTHON3HOME', 'value': '{pkgroot}/lib/python3.8'},
            ],
        },
    }
