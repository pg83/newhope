@ygenerator(tier=-3, kind=['core', 'dev', 'tool'])
def make0(num):
    def it():
        extra = []

        if num >= 4:
            extra.append('--with-libiconv-prefix=$(MNGR_{N}_DIR)'.format(N='DEVTOOLS' + str(num - 1)))
        yield 'source fetch "http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-4.2.tar.gz" 1'
        yield './configure --prefix=$IDIR {extra} || exit 1'.format(extra=' '.join(extra))

        if num == 1:
            yield '$YSHELL ./build.sh'
            yield 'mkdir $IDIR/bin && cp make $IDIR/bin/ && chmod +x $IDIR/bin/make'
        else:
            yield '$YMAKE -j2'
            yield '$YMAKE install'

    return {
        'code': '\n'.join(it()),
        'prepare': '$(ADD_PATH)',
        'version': '4.2',
    }
