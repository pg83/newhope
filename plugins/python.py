def python_base(kind):
    return {
        'code': """
            source fetch "https://www.python.org/ftp/python/{version}/Python-{version}.tar.xz" 1
            export PYTHONHOME=
            $(APPLY_EXTRA_PLAN_0)
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared --with-signal-module --with-system-expat --with-system-ffi || exit1
            ##echo "#define HAVE_PTH 1" >> pyconfig.h
            ##echo "#undef HAVE_PTHREAD_H" >> pyconfig.h 
            $YMAKE -j $NTHRS || exit 1
            $YMAKE install

            mkdir good && cd good
            $(APPLY_EXTRA_PLAN_1)
            $(APPLY_EXTRA_PLAN_2)
            export PYTHONHOME="$IDIR"
            source ./mk_staticpython.sh "$IDIR/bin/python2.7" "2.7" "2" "Py_Main"
        """,
        'version': '2.7.17',
        'extra': [
            {'kind': 'file', 'path': 'Modules/Setup.local', 'data': y.builtin_data('data/Setup.local2')},
            {'kind': 'file', 'path': 'find_modules.py', 'data': y.builtin_data('data/find_modules.py')},
            {'kind': 'file', 'path': 'mk_staticpython.sh', 'data': y.builtin_data('data/mk_staticpython.sh')},
        ],
        'meta': {
            'kind': kind,
            'depends': ['ncurses', 'iconv', 'intl', 'zlib', 'pkg-config-int', 'libffi', 'readline', 'termcap', 'expat', 'sqlite3'],
            'provides': [
                {'lib': 'python2.7'},
                {'env': 'PYTHON', 'value': '{pkgroot}/bin/staticpython2'},
                {'env': 'PYTHONHOME', 'value': '{pkgroot}/lib/python2.7'},
            ],
        },
    }


@y.ygenerator()
def python0():
    return python_base(['tool'])


@y.ygenerator()
def python_pth0():
    r = y.dc(python_base(['tool']))

    r['code'] = r['code'].replace('./configure', './configure --with-pth').replace('##', '')
    r['meta']['depends'].append('pth')
    r['meta']['env'] = [
        ('PTH', '--with-pth'),
    ]

    return r
