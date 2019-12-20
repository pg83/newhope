@y.ygenerator()
def git0():
    return {
        'code': """
             source fetch "https://mirrors.edge.kernel.org/pub/software/scm/git/git-{version}.tar.xz" 1
             
             curl_dir=$(dirname "$CURL")
             curl_dir=$(dirname "$curl_dir")
             expat_dir=$(echo "$CMAKE_PREFIX_PATH" | tr ':' '\n' | grep 'tow-expat')

             export CFLAGS="-w -Icompat/regex $CFLAGS"
             export CPPFLAGS="-w -Icompat/regex $CPPFLAGS"

             run_make() {
                 $YMAKE -j $NTHRS V=1 PERL_PATH="$YPERL" DESTDIR="$IDIR" PREFIX="$IDIR" USE_LIBPCRE1=1 SHELL_PATH="$YSHELL" CURLDIR="$curl_dir" CURL_LDFLAGS="$LDFLAGS $LIBS" EXPATDIR="$expat_dir" NO_GETTEXT=1 NO_FINK=1 NO_DARWIN_PORTS=1 NO_TCLTK=1 PYTHON_PATH="$PYTHON" HAVE_DEV_TTY=1 DEFAULT_EDITOR="\$EDITOR" NO_REGEX=1 CC="$CC" AR="$AR" RANLIB="$RANLIB" LDFLAGS="$LDFLAGS $LIBS" $@
             }

             run_make all man
             run_make install install-man
        """,
        'version': '2.24.1',
        'meta': {
            'kind': ['tool'],
            'depends': ['pcre', 'curl', 'openssl', 'expat', 'python', 'iconv', 'perl5'],
            'provides': [
                {'env': 'GIT', 'value': '{pkgroot}/bin/git'},
                {'env': 'GIT_EXEC_PATH', 'value': '{pkgroot}/bin'},
            ],
        },
    }
