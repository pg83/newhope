@y.package
def bash0():
    def do():
        yield '--disable-extended-glob-default'
        yield '--enable-extended-glob'
        yield '--enable-job-control'
        yield '--with-installed-readline'
        yield '--enable-readline'

    return {
        'code': """
            export CFLAGS="-fpermissive $CFLAGS -w"
            export LIBS="$LDFLAGS $LIBS"
            export CFLAGS="$CFLAGS $LIBS -Dsh_unset_nodelay_mode=bash_sh_unset_nodelay_mode -Dsh_get_env_value=bash_sh_get_env_value -Dsh_get_env_value=bash_sh_get_env_value -Dsh_get_home_dir=bash_sh_get_home_dir -Dsh_set_lines_and_columns=bash_sh_set_lines_and_columns -Dxfree=bash_xfree -Dsh_single_quote=bash_sh_single_quote"
            source fetch "https://ftp.gnu.org/gnu/bash/bash-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --without-bash-malloc --disable-nls  {extra}
            $YMAKE LIBS_FOR_BUILD="$LIBS" -j $NTHRS
            $YMAKE install
        """.replace('{extra}', ' '.join(do())),
        'meta': {
            'kind': ['tool'],
            'depends': ['ncurses', 'intl', 'iconv', 'make', 'c'],
            'provides': [
                {'tool': 'YBASH', 'value': '{pkgroot}/bin/bash'},
            ],
        }
    }
