@ygenerator(tier=2, kind=['core', 'dev', 'tool'])
def bash0(num):
    def do():
        if num >= 5:
            yield '--with-installed-readline=$(MNGR_{N}_DIR)'.format(N='DEVTOOLS' + str(num - 1))

        yield '--disable-extended-glob'
        yield '--disable-extended-glob-default'
        yield '--enable-minimal-config'

        if num >= 4:
            yield '--with-libintl-prefix=$(MNGR_{N}_DIR)'.format(N='DEVTOOLS' + str(num - 1))
            yield '--enable-job-control'
            yield '--with-curses=$(MNGR_{N}_DIR)'.format(N='DEVTOOLS' + str(num - 1))

    return {
        'code': """
            export CFLAGS="-fpermissive $CFLAGS -w"
            source fetch "https://ftp.gnu.org/gnu/bash/bash-5.0.tar.gz" 1
            ./configure --prefix=$IDIR --without-bash-malloc --disable-nls  {extra}
            $YMAKE
            $YMAKE install
        """.format(extra=' '.join(do())),
        'version': '5.0',
    }
