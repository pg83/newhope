@ygenerator(tier=1, kind=['core', 'dev', 'library', 'tool'])
def libarchive0(num, info):
    version = '3.4.0'
    name = 'libarchive'
    url = 'https://libarchive.org/downloads/' + name + '-' + version + '.tar.gz'

    return {
        'code': """
             source fetch "{url}" 1
             ./configure --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j2
             $YMAKE install
        """.replace('{url}', url),
        'version': version,
    }
