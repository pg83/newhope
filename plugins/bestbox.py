@y.ygenerator()
def bestbox0():
    return {
        'os': 'linux',
        'code': """
            mkdir -p $IDIR/bin

            cp $TOYBOX $IDIR/bin
            cp $BUSYBOX $IDIR/bin            
            cd $IDIR/bin

            for i in `./toybox`; do
                ln -fs ./toybox ./$i
            done

            for x in `./busybox --list-full`; do
                y=$(basename $x)
                ln -s -f ./busybox $y
            done            
        """,
        'meta': {
            'kind': ['tool'],
            'depends': ['busybox', 'toybox'],
            'contains': ['busybox', 'toybox'],
            'provides': [
                {'env': 'YGZIP', 'value': '{pkgroot}/bin/gzip'},
                {'env': 'YTAR', 'value': '{pkgroot}/bin/tar'},
                {'env': 'YWGET', 'value': '{pkgroot}/bin/wget'},
                {'env': 'TOYBOX', 'value': '{pkgroot}/bin/toybox'},
                {'env': 'BUSYBOX', 'value': '{pkgroot}/bin/busybox'},
            ],
        },  
    }


@y.ygenerator()
def superbox0():
    data = y.deep_copy(bestbox0())
    data['meta']['provides'].append({'env': 'COREUTILS', 'value': '{pkgroot}/bin/coreutils'})
    data['meta']['kind'].append('box')
    data['meta']['depends'] += ['coreutils']
    data['meta']['contains'] = ['bestbox', 'busybox', 'toybox', 'coreutils']
    data['code'] += """
            cp $COREUTILS $IDIR/bin/
            cd $IDIR/bin/
            progs=$(./coreutils --help | tr '\n' ' ' | sed -e 's/.*\[//' | sed -e 's/ Use: .*//') 
        
            for i in $progs; do 
                ln -sf ./coreutils $i
            done
"""

    return data
