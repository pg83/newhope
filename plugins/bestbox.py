@y.ygenerator()
def bestbox0():
    return {
        'os': 'linux',
        'code': """
            mkdir -p $IDIR/bin

            cp $TOYBOX $IDIR/bin
            cp $BUSYBOX $IDIR/bin
            
            cd $IDIR/bin

            for x in `./busybox --list-full`; do
                y=$(basename $x)
                ln -s -f ./busybox $y
            done            

            for i in `./toybox`; do
                ln -fs ./toybox ./$i
            done
        """,
        'meta': {
            'kind': ['tool', 'box'],
            'depends': ['busybox', 'toybox'],
            'provides': [
                {'env': 'YGZIP', 'value': '{pkgroot}/bin/gzip'},
                {'env': 'YTAR', 'value': '{pkgroot}/bin/tar'},
                {'env': 'YWGET', 'value': '{pkgroot}/bin/wget'},
            ],
        },        
    }
