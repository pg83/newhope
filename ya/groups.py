def tini_group():
    return [
        'toybox-run',
        'busybox-run',
        'coreutils-run',
        'dash-run',
        'tar-run',
        'upm-run',
    ]


def compression_group():
    return [
        'xz-run',
        'gzip-run',
        'bzip2-run',
        'unrar-run',
        'tar-run',
        'p7zip-run',
        'upx-run',
    ]


def textutils_group():
    return [
        'gawk-run',
        'grep-run',
        'sed-run',
        'file-run',
        'diffutils-run',
        'less-run',
    ]


def small_group():
    return [
        '@tini',
        '@compression',
        '@textutils',
        'bc-run',
        'curl-run',
        'psmisc-run',
        'procps-ng-run',
        'vim-run',
        'findutils-run',
    ]


def full_group():
    return [
        '@small',
        'mc-slang',
        'openssh',
    ]

def devel_group():
    return [
        '@full',
        'make-run',
        'sqlite3-run',
        'ninja-run',
        'cmake',
        'patch-run',
        'bison',
        'git',
        'python3',
    ]
