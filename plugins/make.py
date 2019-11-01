@ygenerator(tier=-2, kind=['core', 'dev', 'tool'], cached=['num', 'deps', 'codec'])
def make0(num, deps, codec):
    def it():
        extra = []

        if num >= 4:
            extra.append('--with-libiconv-prefix=$(MNGR_{N}_DIR)'.format(N='DEVTOOLS' + str(num - 1)))

        yield './configure --prefix=$IDIR {extra} || exit 1'.format(extra=' '.join(extra))

        if num > 1:
            yield '$YSHELL ./build.sh'
            yield 'mkdir $IDIR/bin && cp make $IDIR/bin/ && chmod +x $IDIR/bin/make'
        else:
            yield '$YMAKE -j2'
            yield '$YMAKE install'

    return {
        'code': '\n'.join(it()),
        'src': 'http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-4.2.tar.gz',
        'prepare': '$(ADD_PATH)',
        'codec': codec,
        'deps': deps,
        'version': '4.2',
    }
