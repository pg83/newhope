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
        'p7zip',
        'pkg-config',
        'm4',
        'sed',
        'sqlite3',
        'tar',
        'unrar',
        'xz',
        'yash',
        'psmisc',
        'python3-static',
        'bc',
    ]

    lst_run = [x + '-run' for x in lst]

    return {
        'code': '''
             copy_many() {
                 shift
                 shift
 
                 no_busybox="$(echo $@ | tr ' ' '\n' | grep -v busybox)"
                 busybox="$(echo $@ | tr ' ' '\n' | grep busybox)"
 
                 for i in $no_busybox $busybox; do
                      (cd $(dirname $i) && $YTAR -v -cf - .) | (cd $IDIR/ && $YTAR -v -Uxf -)
                 done
             }

             copy_many $@

             rm -rf $IDIR/include
             rm -rf $IDIR/share
             rm -rf $IDIR/lib
             rm -rf $IDIR/tools
             cd $IDIR/bin
             ln -sf bsdtar tar 
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': lst_run,
            'contains': lst_run + lst,
            'provides': [
                {'env': 'SED', 'value': '{pkgroot}/bin/sed'},
                {'env': 'YGNUTAR', 'value': '{pkgroot}/bin/tar'},
                {'env': 'YTAR', 'value': '{pkgroot}/bin/bsdtar'},
                {'env': 'YBSDTAR', 'value': '{pkgroot}/bin/bsdtar'},
                {'env': 'YXZ', 'value': '{pkgroot}/bin/xz'},
                {'env': 'YXZCAT', 'value': '{pkgroot}/bin/xzcat'},
                {'env': 'STATICPYTHON3', 'value': '{pkgroot}/bin/staticpython3'},
            ],
        }
    }
