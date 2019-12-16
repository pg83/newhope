def make_impl(boot, deps, contains, kind):
    def it():
        if '/test1' in y.verbose:
            raise Exception('test')

        yield 'source fetch "http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-{version}.tar.gz" 1'
        yield '$YSHELL ./configure --prefix=$IDIR --disable-load || exit 1'

        if boot:
            yield '$YSHELL ./build.sh'
            yield 'mkdir $IDIR/bin && cp make $IDIR/bin/ && chmod +x $IDIR/bin/make'
        else:
            yield '$YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-load || exit 1'
            yield '$YMAKE -j $NTHRS'
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
    return make_impl(True, ['musl-boot'], [], [])


@y.ygenerator()
def make0():
    return make_impl(False, ['musl', 'make-boot'], ['make-boot'], ['box'])
