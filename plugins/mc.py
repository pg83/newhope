mc_sh = '''#!/bin/sh
. /etc/profile
if test -z "$HOME"; then
    HOME=$(getent passwd `whoami` | cut -d: -f6)
fi
export TMPDIR="$HOME/.mctmpdir"
mkdir -p "$TMPDIR" || true
exec mc.real "$@"
'''

def mc(gui, gui_lib):
    return {
        'code': '''
             source fetch "http://ftp.midnight-commander.org/mc-{version}.tar.xz" 1
             export LDFLAGS="$LDFLAGS $LIBS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-screen={gui}  || exit 1
             $YMAKE -j $NTHRS
             echo 'all install:' > doc/hlp/Makefile
             $YMAKE install

             cd $IDIR/bin
             mv mc mc.real
             $(APPLY_EXTRA_PLAN_0)
             chmod +x mc
        '''.replace('{gui}', gui_lib),
        'version': '4.8.23',
        'extra': [
            {'kind': 'file', 'path': 'mc', 'data': mc_sh},
        ],
        'meta': {
            'kind': ['program'],
            'depends': ['intl', 'iconv', 'glib', gui, 'make', 'c'],
        }
    }


@y.package
def mc_slang0():
    return mc('slang', 'slang')


@y.package
def mc_ncurses0():
    return mc('ncurses', 'ncurses')
