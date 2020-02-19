@y.package
def cmake0():
    extra = []

    if '{os}' == 'linux':
        extra = ['kernel-h']

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
             $YUPX $IDIR/bin/cmake
             $YUPX $IDIR/bin/cpack
             $YUPX $IDIR/bin/ctest
        """,
        'version': '3.16.1',
        'meta': {
            'kind': ['tool'],
            'depends': [
                'c++',
                'zlib',
                'bzip2',
                'xz',
                'libarchive',
                'expat',
                'dl',
                'iconv',
                'make',
                'c',
                'upx',
            ] + extra,
            'provides': [
                {'env': 'CMAKE', 'value': '{pkgroot}/bin/cmake'},
            ],
        }
    }
