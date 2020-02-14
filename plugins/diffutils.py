@y.package
def diffutils0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/diffutils/diffutils-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-gcc-warnings || exit 1
             #(cd man && echo '#!'"$YPERL -w" > tmp && cat help2man >> tmp && mv tmp help2man && chmod +x help2man)
             (cd man && echo 'all install:' > Makefile)
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '3.7',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['iconv', 'intl', 'libsigsegv', 'perl5', 'help2man', 'make', 'c']
        },
    }
