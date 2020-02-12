def tini_distr():
    return [
        'toybox-run',
        'busybox-boot-run',
        'coreutils-run',
        'yash-run',
    ]


def small_distr():
    return [
        '@tini',
        'dash-run',
        'xz-run',
        'curl-run',
        'gzip-run',
        'bzip2-run',
        'unrar-run',
        'gawk-run',
        'grep-run',
        'make-run',
        'sed-run',
        'bsdtar-run',
        'file-run',
        'upm-run',
        'psmisc-run',
        'bc-run',
        'p7zip-run',
        'diffutils-run',
        'less-run',
    ]


def common_distr():
    return [
        '@small',
        'mc-slang',
        'mc-ncurses',
        'cmake',
        'openssl',
        'sqlite3-run',
        'ninja-run',
        'dropbear',
    ]


def misc_distr():
    return [
        'gnu-m4',
        'python3-static',
        'pkg-config',
        'toybox',
        'pcre1',
        #'clang'
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
    return common_distr() + misc_distr() + ['base']


def all_distro_packs():
    return list(resolve_packs(all_packs_0()))
