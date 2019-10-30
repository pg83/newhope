@ygenerator(tier=1, kind=['core', 'dev', 'library', 'tool'], cached=['deps', 'num', 'info'])
def libarchive0(deps, num, info):
    version = '3.4.0'
    name = 'libarchive'
    url = 'https://libarchive.org/downloads/' + name + '-' + version + '.tar.gz'

    return {
        'code': """
             source fetch "{url}"
             ./configure --prefix=$IDIR --enable-static --disable-shared
             make -j2
             make install
        """.replace('{url}', url),
        'version': version,
        'deps': deps,
    }
