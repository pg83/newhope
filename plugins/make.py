@y.ygenerator(tier=-3, kind=['box'])
def make0():
    def it():
        if '/test1' in y.verbose:
            raise Exception('test')

        yield 'source fetch "http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-4.2.tar.gz" 1'

        yield '$YSHELL ./configure --prefix=$IDIR || exit 1'
        yield '$YSHELL ./build.sh'
        yield 'mkdir $IDIR/bin && cp make $IDIR/bin/ && chmod +x $IDIR/bin/make'

        yield 'export YMAKE=$IDIR/bin/make'

        yield '$YSHELL ./configure $COFLAGS --prefix=$IDIR || exit 1'
        yield '$YMAKE -j2'
        yield '$YMAKE install'

    return {
        'code': '\n'.join(it()),
        'version': '4.2',
        'meta': {
            'soft': ['iconv', 'intl'],
        },
    }

