def python_base(kind):
    return {
        'code': """
            source fetch "https://www.python.org/ftp/python/{version}/Python-{version}.tar.xz" 1
            $(APPLY_EXTRA_PLAN_0)
            $(APPLY_EXTRA_PLAN_1)
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --with-system-libmpdec --enable-static --disable-shared --with-signal-module --with-system-ffi || exit1
            $YMAKE -j $NTHRS || exit 1
            ./python.exe ./fix.py patch ./setup.py
            DUMP=1 ./python.exe ./setup.py build > data.json
            ./python.exe ./fix.py ./data.json > Modules/Setup.local
            $YMAKE -j $NTHRS || exit 1
            $YMAKE -j $NTHRS || exit 1
            $YMAKE install
            cp -R Tools $IDIR/
            mv $IDIR/Tools $IDIR/tools 
        """,
        'version': '3.8.0',
        'extra': [
            {'kind': 'file', 'path': 'Modules/Setup', 'data': y.globals.by_name['data/Setup.local']['data']},
            {'kind': 'file', 'path': 'fix.py', 'data': y.globals.by_name['data/python3_bc.py']['data']},
        ],
        'meta': {
            'kind': kind,
            'depends': [
                'ncurses', 'iconv', 'intl', 'zlib',
                'pkg-config', 'libffi', 'readline',
                'termcap', 'mpdecimal', 'xz', 'bzip2',
                'sqlite3', 'openssl',
            ],
            'provides': [
                {'lib': 'python3.8'},
                {'env': 'PYTHON3', 'value': '{pkgroot}/bin/python'},
            ],
        },
    }


@y.ygenerator()
def python30():
    return python_base(['box', 'tool'])
