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
    ]

    lst_run = [x + '-run' for x in lst]

    return {
        'code': '''
             copy_many() {
                 shift
                 shift
                 for i in $@; do
                      (cd $(dirname $i) && $YTAR -v -cf - .) | (cd $IDIR/ && $YTAR -v -Uxf -)
                 done
             }

             copy_many $@

             rm -rf $IDIR/include
             rm -rf $IDIR/share
             rm -rf $IDIR/lib
             rm -rf $IDIR/tools 
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
            ],
        }
    }
