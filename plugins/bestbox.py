#if defined(__LINUX__)
    @y.package
    def bestbox0():
        return {
            'code': """
                mkdir -p $IDIR/bin

                cp $TOYBOX $IDIR/bin
                cp $BUSYBOX $IDIR/bin
                cd $IDIR/bin

                for i in `./toybox`; do
                    ln -fs toybox $i
                done

                for x in `./busybox --list-full`; do
                    y=$(basename $x)
                    ln -fs busybox $y
                done
            """,
            'meta': {
                'kind': ['tool'],
                'depends': ['busybox', 'toybox'],
                'undeps': ['make', 'musl'], 
                'contains': ['busybox', 'toybox'],
                'provides': [
                     {'env': 'YGZIP', 'value': '{pkgroot}/bin/gzip'},
                     {'env': 'YTAR', 'value': '{pkgroot}/bin/tar'},
                     {'env': 'YWGET', 'value': '{pkgroot}/bin/wget'},
                     {'env': 'TOYBOX', 'value': '{pkgroot}/bin/toybox'},
                     {'env': 'BUSYBOX', 'value': '{pkgroot}/bin/busybox'},
                     {'env': 'YSHELL', 'value': '{pkgroot}/bin/sh'},
                ],
            },  
        }

    @y.package
    def superbox0():
        data = y.dc(bestbox0())
        data['os'] = 'linux'
        data['meta']['provides'].append({'env': 'COREUTILS', 'value': '{pkgroot}/bin/coreutils'})
        data['meta']['provides'].append({'env': 'DASH', 'value': '{pkgroot}/bin/dash'})
        data['meta']['kind'].append('box')
        data['meta']['depends'] += ['coreutils', 'dash']
        data['meta']['contains'] = ['bestbox', 'busybox', 'toybox', 'coreutils', 'dash']
        data['code'] += '''
            cp "$COREUTILS" "$IDIR/bin/"
            cd "$IDIR/bin/"
            progs=$(./coreutils --help | tr '\\n' ' ' | sed -e 's/.*\[//' | sed -e 's/ Use: .*//') 

            for i in $progs; do 
                ln -fs coreutils $i
            done

            cp "$DASH" "$IDIR/bin/"
            cd "$IDIR/bin/"
            ln -fs dash sh
        '''

        return data
#endif
