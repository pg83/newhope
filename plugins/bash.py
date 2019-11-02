@ygenerator(tier=-1, kind=['core', 'dev', 'tool'])
def bash0(deps, num):
    def do():
        if num >= 5:
            #yield '--disable-history'
            #yield '--enable-readline'
            yield '--with-installed-readline=$(MNGR_{N}_DIR)'.format(N='DEVTOOLS' + str(num - 1))

        yield '--disable-extended-glob'
        yield '--disable-extended-glob-default'
        yield '--enable-minimal-config'

        if num >= 4:
            yield '--with-libintl-prefix=$(MNGR_{N}_DIR)'.format(N='DEVTOOLS' + str(num - 1))
            yield '--enable-job-control'
            yield '--with-curses=$(MNGR_{N}_DIR)'.format(N='DEVTOOLS' + str(num - 1))
            #'--with-included-gettext'

    return {
        'code': """
            export CFLAGS="-fpermissive $CFLAGS -w"
            source fetch "https://ftp.gnu.org/gnu/bash/bash-5.0.tar.gz" 1
            ./configure --prefix=$IDIR --without-bash-malloc --disable-nls  {extra}
            $YMAKE
            $YMAKE install
        """.format(extra=' '.join(do())),
        'prepare': '$(ADD_PATH)',
        'deps': deps,
        'version': '5.0'
    }
