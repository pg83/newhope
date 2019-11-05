@ygenerator(tier=2, kind=['core', 'dev', 'tool'])
def diffutils0(num):
    version = '3.7'
    url = 'https://ftp.gnu.org/gnu/diffutils/diffutils-' + version + '.tar.xz'
    func = eval('y.devtools' + str(num - 1))

    return {
        'code': """
             export CFLAGS="$CFLAGS -fno-builtin"
             export LIBS='-framework CoreFoundation -liconv -lintl'
             ./configure --prefix=$IDIR --disable-gcc-warnings --with-libiconv-prefix=$(MNGR_{name}_DIR) --with-libintl-prefix=$(MNGR_{name}_DIR) || exit 1
             $YMAKE -j2
             $YMAKE install
        """.format(name=func.__name__.upper()),
        'url': url,
        'version': version,
    }
