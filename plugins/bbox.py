@y.package
def box0():
    lst = [
        'busybox',
        'coreutils',
        'asciidoc',
        'bison',
        'bzip2',
        'curl',
        'dash',
        'diffutils',
        'gawk',
        'gettext',
        'grep',
        'gzip',
        'help2man',
        'libarchive',
        'libiconv',
        'make',
        'ninja',
        'pkg-config',
        'm4',
        'sed',
        'sqlite3',
        'tar',
        'unrar',
        'xz',
        'psmisc',
        'bc',
        'patch',
        'procps-ng',
        'wget',
    ]

    lst_run = [x + '-run' for x in lst]

    return {
        'code': '''
             copy_many() {
                 shift
                 shift
 
                 no_busybox="$(echo $@ | tr ' ' '\\n' | grep '\\-run\\-' | grep -v busybox | tr '\\n' ' ')"
                 busybox="$(echo $@ | tr ' ' '\\n' | grep '\\-run\\-' | grep busybox)"
 
                 for i in $busybox $no_busybox; do
                      (cd $(dirname $i) && $YTAR -v -cf - .) | (cd $IDIR/ && $YTAR -v -Uxf -)
                 done
             }

             copy_many $@

             cp -p $YUPX $IDIR/bin/upx

             rm -rf $IDIR/include
             rm -rf $IDIR/share
             rm -rf $IDIR/lib
             rm -rf $IDIR/tools
             cd $IDIR/bin
             ln -sf bsdtar tar 
             ln -sf dash sh
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': lst_run + ['upx'],
            'contains': lst_run + lst + ['upx', 'make-boot', 'busybox-boot', 'busybox', 'toybox'],
            'repacks': {},
            'provides': [
                {'tool': 'SED', 'value': '"{pkgroot}/bin/sed"'},
                {'tool': 'YGNUTAR', 'value': '"{pkgroot}/bin/tar"'},
                {'tool': 'YTAR', 'value': '"{pkgroot}/bin/bsdtar"'},
                {'tool': 'YBSDTAR', 'value': '"{pkgroot}/bin/bsdtar"'},
                {'tool': 'YXZ', 'value': '"{pkgroot}/bin/xz"'},
                {'tool': 'YXZCAT', 'value': '"{pkgroot}/bin/xzcat"'},
                {'tool': 'YUPX', 'value': '"{pkgroot}/bin/upx"'},
                {'tool': 'YMAKE', 'value': '"{pkgroot}/bin/make"'},
                {'tool': 'YSHELL', 'value': '"{pkgroot}/bin/dash"'},
                {'tool': 'YGZIP', 'value': '"{pkgroot}/bin/gzip"'},
                {'tool': 'YBZIP2', 'value': '"{pkgroot}/bin/bzip2"'},
                #{'tool': 'YUNZIP', 'value': '"{pkgroot}/bin/dash"'},
                {'tool': 'YCURL', 'value': '"{pkgroot}/bin/curl"'},
                {'tool': 'YWGET', 'value': '"{pkgroot}/bin/wget"'},
                {'tool': 'Y7ZA', 'value': '"{pkgroot}/bin/7za"'},
            ],
        }
    }
