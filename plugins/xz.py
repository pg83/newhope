@ygenerator(tier=0, kind=['core', 'tool', 'library'])
def xz0():
    return {
        'code': """
             source fetch "https://sourceforge.net/projects/lzmautils/files/xz-5.2.4.tar.gz/download" 1
             $YSHELL ./configure --prefix=$IDIR --disable-shared --enable-static && $YMAKE -j2 && $YMAKE install
        """,
        'version': '5.2.4',
    }
