def tini_distr():
    return [
        'toybox-run',
        'busybox-run',
        'coreutils-run',
        'dash-run',
    ]


def compression_distr():
    return [
        'xz-run',
        'gzip-run',
        'bzip2-run',
        'unrar-run',
        'bsdtar-run',
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
        'yash-run',
        'curl-run',
        'psmisc-run',
    ]


def dev_distr():
    return [
        'make-run',
        'sqlite3-run',
        'ninja-run',
        'cmake',
    ]


def common_distr():
    return [
        '@small',
        'mc-slang',
        'mc-ncurses',
    ]


def misc_distr():
    return [
        'base',
        'gnu-m4',
        'python3-static',
        'pkg-config',
        'toybox',
        'pcre1',
        'openssl',
        'dropbear',
        'bc',
        'upm',
        'upm-run',
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
    return common_distr() + dev_distr() + misc_distr() + ['base']


def all_distro_packs():
    return list(resolve_packs(all_packs_0()))
