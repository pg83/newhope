@y.ygenerator()
def cmake0():
    return {
        'code': """
             source fetch "https://github.com/Kitware/CMake/releases/download/v{version}/cmake-{version}.tar.gz" 1
             export CFLAGS="-w $CFLAGS $LDFLAGS $LIBS"
             export CXXFLAGS="-w $CXXFLAGS $LDFLAGS $LIBS"
             $YSHELL ./bootstrap --system-expat --system-zlib --system-bzip2 --system-liblzma --system-libarchive --prefix=$IDIR --parallel=$NTHRS -- -DCMAKE_USE_OPENSSL=OFF -Dfortran=OFF -DBUILD_TESTING=OFF || true
             echo > .clang-tidy
             ./Bootstrap.cmk/cmake .
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '3.16.1',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['c++', 'zlib', 'bzip2', 'xz', 'libarchive', 'kernel-h', 'expat'],
            'provides': [
                {'env': 'CMAKE', 'value': '{pkgroot}/bin/cmake'},
            ],
        }
    }
