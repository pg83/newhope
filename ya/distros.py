def tini_distr():
    return [
        'toybox-run',
        'busybox-run',
        'coreutils-run',
        'yash-run',
    ]


def small_distr():
    return [
        '@tini',
        'dash-run',
        'xz-run',
        'curl',
        'gzip-run',
        'bzip2-run',
        'unrar-run',
        'gawk',
        'grep-run',
        'make-run',
        'sed-run',
        'bsdtar-run',
        'file-run',
        #'man-db',
        'python3',
        'upm',
    ]

def common_distr():
    return [
        '@small',
        'mc-slang',
        'mc-ncurses',
        'p7zip-run',
        'cmake',
        'openssl',
        'sqlite3-run',
        'diffutils-run',
        'ninja-run',
        'pkg-config',
    ]


def dev_distr():
    return [
        #'clang',
    ]


def distr_by_name(name):
    return y.find(name + '_distr')()


def resolve_packs(packs):
    for p in packs:
        if p[0] == '@':
            yield from resolve_packs(distr_by_name(p[1:]))
        else:
            yield p


def all_packs_0():
    return common_distr() + dev_distr() + ['base']


def all_distro_packs():
    return list(resolve_packs(all_packs_0()))
