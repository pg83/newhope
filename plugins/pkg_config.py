@ygenerator(tier=0, kind=['core', 'dev', 'tool'])
def pkg_config0(num, info):
    if num <= 6:
        extra = '--with-internal-glib'
    else:
        extra = ''

    return {
        'code': """
            source fetch "https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz" 1
            export LIBS="-liconv -lcharset"
            ./configure --prefix=$IDIR {extra} --enable-static --disable-shared
            $YMAKE
            $YMAKE install
        """.format(extra=extra),
        'version': '0.29.2',
    }
