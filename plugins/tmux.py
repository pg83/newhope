@y.package
def tmux0():
    return {
        'code': '''
            source fetch "https://github.com/tmux/tmux/releases/download/{version}/tmux-{version}-rc.tar.gz" 1

            mkdir sys
            echo > sys/queue.h

            export CFLAGS="-I$(pwd) -I$LIBEVENT_ROOT/include $CFLAGS"

            export LIBEVENT_CFLAGS="$CFLAGS"
            export LIBEVENT_LIBS="$LIBS"

            export LIBTINFO_CFLAGS="$CFLAGS"
            export LIBTINFO_LIBS="$LIBS"

            export LIBNCURSES_CFLAGS="$CFLAGS"
            export LIBNCURSES_LIBS="$LIBS"

            $YSHELL ./configure --prefix=$IDIR --enable-utf8proc --enable-static --disable-shared || exit 1
            $YMAKE -j $NTHRS
            $YMAKE install
        ''',
        'version': '3.1',
        'meta': {
            'depends': ['make', 'c', 'libevent', 'ncurses', 'utf8proc'],
            'provides': [
                {'tool': 'TMUX_BIN', 'value': '"{pkgroot}/bin/tmux"'},
            ],
        },
    }
