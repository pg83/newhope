@y.package
def upx0():
    return {
        'code': '''
            source fetch "https://github.com/upx/upx/releases/download/v{version}/upx-{version}-amd64_linux.tar.xz" 1
            mkdir $IDIR/bin
            cp -p upx $IDIR/bin 
        ''',
        'code1': '''
            source fetch "https://github.com/upx/upx/releases/download/v{version}/upx-{version}-src.tar.xz" 1
            cd src
            $YMAKE CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS" LIBS="$LIBS" CC="$CC" CXX="$CXX" UPX_UCLDIR="$UPX_UCLDIR" -j $NTHRS
            mkdir $IDIR/bin
            chmod +x upx.out
            upx.out -o $IDIR/bin/upx ./upx.out
        ''',
        'version': '3.96',
        'meta': {
            'kind': ['tool'],
            'depends': ['zlib', 'ucl', 'make', 'c', 'c++'],
            'provides': [
                {'env': 'YUPX', 'value': '"{pkgroot}/bin/upx"'},
            ]
        },
    }
