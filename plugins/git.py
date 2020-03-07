@y.package
def git0():
    return {
        'code': """
             source fetch "https://mirrors.edge.kernel.org/pub/software/scm/git/git-{version}.tar.xz" 1

             export CFLAGS="$OPENSSL_INCLUDES $LIBPCRE2_INCLUDES -w -Icompat/regex -iquote$(pwd) $CFLAGS"
             export CPPFLAGS="$OPENSSL_INCLUDES -w -Icompat/regex $CPPFLAGS"
             export LDFLAGS="$LDFLAGS $LIBS"

             ln -s $PYTHON ./python 
             export PATH="$(pwd):$PATH"

             $YSHELL ./configure --prefix="$IDIR" --with-python=$PYTHON --with-perl=$YPERL --with-shell=$YSHELL --with-libpcre2

             $YMAKE -j $NTHRS
             $YMAKE install

             ($YUPX $IDIR/bin/*) || true
             ($YUPX $IDIR/libexec/git-core/*) || true
        """,
        'meta': {
            'depends': ['upx', 'pcre', 'curl', 'openssl', 'expat', 'python', 'iconv', 'perl5', 'zlib', 'make', 'c'],
            'provides': [
                {'tool': 'GIT', 'value': '{pkgroot}/bin/git'},
                {'tool': 'GIT_EXEC_PATH', 'value': '{pkgroot}/bin'},
            ],
            'repacks': {},
        },
    }
