@ygenerator(tier=0, kind=['core', 'dev', 'tool'])
def pkg_config0(deps, num, info):
    extra_flags = ''
    dep = []

    if num > 1005:
        extra = ''
        dep = [eval('y.glib5')(info)]
        extra_flags = 'export CFLAGS="-I$(MNGR_GLIB5_INC_DIR)"; export LDFLAGS="-L$(MNGR_GLIB5_LIB_DIR)"; export PKG_CONFIG_PATH="$(MNGR_GLIB5_DIR)/lib/pkgconfig:$PKG_CONFIG_PATH"; '
    elif num <= 5:
        extra = '--with-internal-glib'
    else:
        extra = ''

    return {
        'code': """
            source fetch "https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz" 1
            export LIBS="-liconv -lcharset"; {extra_flags}
            ./configure --prefix=$IDIR {extra} --enable-static --disable-shared
            $YMAKE
            $YMAKE install
        """.format(extra=extra, extra_flags=extra_flags),
        'deps': dep + deps,
        'prepare': '$(ADD_PATH)',
        'version': '0.29.2',
    }
