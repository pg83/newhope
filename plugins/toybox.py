@helper
def toybox():
    return {
        'code': """
            #pragma cc

            $(FETCH_URL)
            LDFLAGS=--static CFLAGS=-O2 CC=gcc CROSS_COMPILE=$TOOL_CROSS_PREFIX make defconfig toybox
            mv toybox $(INSTALL_DIR)
        """,
        'src': 'http://landley.net/toybox/downloads/toybox-0.8.1.tar.gz',
    }
