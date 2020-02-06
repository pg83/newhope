def small_distr():
    return [
        'busybox',
        'toybox',
        'coreutils',
        'dash',
        'xz',
        'curl',
        'gzip',
        'bzip2',
        'gawk',
        'grep',
        'make',
        'sed',
        'bsdtar',
    ]

def common_distr():
    return [
        'mc-slang',
        'mc-ncurses',
        'yash',
        'p7zip',
        'unrar',
        'bsdtar',
        'python3',
        'cmake',
        'openssl',
        'sqlite3',
        'diffutils',
        'file',
        'ninja',
        'pkg-config',
    ]


def distr_by_name(name):
    return y.find(name + '_distr')


def all_distros():
    return small_distr() + common_distr() + ['base']
