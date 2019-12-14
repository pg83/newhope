def make_impl(deps, contains, kind):
    def it():
        if '/test1' in y.verbose:
            raise Exception('test')

        yield 'source fetch "http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-{version}.tar.gz" 1'

        yield '$YSHELL ./configure --prefix=$IDIR --disable-load || exit 1'
        yield '$YSHELL ./build.sh'
        yield 'mkdir $IDIR/bin && cp make $IDIR/bin/ && chmod +x $IDIR/bin/make'

        yield 'export YMAKE=$IDIR/bin/make'

        yield '$YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-load || exit 1'
        yield '$YMAKE -j4'
        yield '$YMAKE install'

    return {
        'code': '\n'.join(it()),
        'version': '4.2',
        'meta': {
            'kind': ['tool'] + kind,
            'depends': deps,
            'contains': contains,
            'soft': ['iconv', 'intl'],
            'provides': [
                {'env': 'YMAKE', 'value': '{pkgroot}/bin/make'},
            ],
        },
    }


@y.ygenerator()
def make_boot0():
    return make_impl(['musl-boot'], [], [])


@y.ygenerator()
def make0():
    return make_impl(['musl'], ['make-boot'], ['box'])
