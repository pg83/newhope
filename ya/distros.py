def tini_distr():
    return [
        'toybox-run',
        'busybox-run',
        'coreutils-run',
        'dash-run',
        'tar-run',
        'upm-run',
    ]


def compression_distr():
    return [
        'xz-run',
        'gzip-run',
        'bzip2-run',
        'unrar-run',
        'tar-run',
        'p7zip-run',
    ]


def textutils_distr():
    return [
        'gawk-run',
        'grep-run',
        'sed-run',
        'file-run',
        'diffutils-run',
        'less-run',
    ]


def small_distr():
    return [
        '@tini',
        '@compression',
        '@textutils',
        'bc-run',
        'curl-run',
        'psmisc-run',
        'procps-ng-run',
        'vim-run',
    ]


def dev_distr():
    return [
        'make-run',
        'sqlite3-run',
        'ninja-run',
        'cmake',
        'patch',
    ]


def distr_by_name(name):
    return y.find(name + '_distr')()
