@ygenerator(tier=0, kind=['base', 'dev', 'tool'])
def grep0(num):
    if num <= 4:
        pkg = 'export PKG_CONFIG='
    else:
        pkg = ''

    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/grep/grep-3.3.tar.xz" 1
             export CFLAGS="$CFLAGS -fno-builtin"
             {pkg}              
             ./configure --prefix=$IDIR || exit 1
             $YMAKE -j2
             $YMAKE install
        """.format(pkg=pkg),
        'version': '3.3',
    }
