@y.ygenerator()
def cmake0():
    return {
        'code': """
             source fetch "https://github.com/Kitware/CMake/releases/download/v{version}/cmake-{version}.tar.gz" 1
             export CFLAGS="-w $CFLAGS $LDFLAGS $LIBS"
             export CXXFLAGS="-w $CXXFLAGS $LDFLAGS $LIBS"
             $YSHELL ./bootstrap --system-expat --system-zlib --system-bzip2 --system-liblzma --system-libarchive --prefix=$IDIR --parallel=$NTHRS || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '3.16.1',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['c++', 'zlib', 'bzip2', 'xz', 'libarchive', 'kernel-h'],
            'provides': [
                {'env': 'CMAKE', 'value': '{pkgroot}/bin/cmake'},
            ],
        }
    }
