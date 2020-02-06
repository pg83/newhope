def small_distr():
    return [
        'busybox',
        'toybox',
        'coreutils',
        'dash',
        'yash',
        'xz',
        'curl',
        'gzip',
        'bzip2',
        'unrar',
        'gawk',
        'grep',
        'make',
        'sed',
        'bsdtar',
        'file',
    ]

def common_distr():
    return [
        '@small',
        'mc-slang',
        'mc-ncurses',
        'p7zip',
        'python3',
        'cmake',
        'openssl',
        'sqlite3',
        'diffutils',
        'ninja',
        'pkg-config',
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
    return common_distr() + ['base']


def all_distro_packs():
    return list(resolve_packs(all_packs_0()))
