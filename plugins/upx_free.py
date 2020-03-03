@y.package
def upx_free0():
    return {
        'code': '''
            source fetch "https://github.com/upx/upx/releases/download/v{version}/upx-{version}-src.tar.xz" 1
            cd src
            $YMAKE CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS" LIBS="$LIBS" CC="$CC" CXX="$CXX" UPX_UCLDIR="$UPX_UCLDIR" -j $NTHRS
            mkdir $IDIR/bin
            chmod +x upx.out
            upx.out -o $IDIR/bin/upx ./upx.out
        ''',
        'version': y.package_versions()['upx'],
        'meta': {
            'depends': ['zlib', 'ucl', 'make', 'c', 'c++'],
            'provides': [
                {'tool': 'YUPX', 'value': '"{pkgroot}/bin/upx"'},
            ]
        },
    }
