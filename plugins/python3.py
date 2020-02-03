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

            cat Setup | sed -e 's/OPENSSL_INCLUDES/$OPENSSL_INCLUDES/' | sed -e 's/LIBFFI_CFLAGS/$LIBFFI_CFLAGS/' > tmp
            cp tmp Modules/Setup

            $YSHELL ./configure $COFLAGS --prefix=$IDIR --with-system-libmpdec --enable-static --disable-shared --with-signal-module --with-system-ffi || exit1

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

            mkdir good && cd good
            $(APPLY_EXTRA_PLAN_2)
            $(APPLY_EXTRA_PLAN_3)
            source ./mk_staticpython.sh "$IDIR/bin/python{ver}" "{ver}" "3" "Py_BytesMain"
        """.replace('{ver}', ver),
        'version': version,
        'extra': [
            {'kind': 'file', 'path': 'Setup', 'data': y.builtin_data('data/Setup.local')},
            {'kind': 'file', 'path': 'fix.py', 'data': y.builtin_data('data/python3_bc.py')},
            {'kind': 'file', 'path': 'find_modules.py', 'data': y.builtin_data('data/find_modules.py')},
            {'kind': 'file', 'path': 'mk_staticpython.sh', 'data': y.builtin_data('data/mk_staticpython.sh')},
        ],
        'meta': {
            'kind': ['tool', 'box'],
            'depends': [
                'ncurses', 'iconv', 'intl', 'zlib',
                'pkg-config', 'libffi', 'readline',
                'termcap', 'mpdecimal', 'xz', 'bzip2',
                'sqlite3', 'openssl', 'dl',
            ],
            'provides': [
                {'lib': 'python3.8'},
                {'env': 'PYTHON3', 'value': '{pkgroot}/bin/staticpython3'},
                {'env': 'PYTHON3HOME', 'value': '{pkgroot}/lib/python3.8'},
            ],
        },
    }
