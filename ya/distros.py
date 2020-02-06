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
        '@small'
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
    return y.find(name + '_distr')


def resolve_distr_0(name):
    if name[0] == '@':
        yield from resolve_distr_0(name[1:])

    for x in distr_by_name(name):
        yield from resolve_distr_0(x)


def resolve_distr(name):
    return list(resolve_distr_0())


def all_distros():
    return common_distr() + ['base']
