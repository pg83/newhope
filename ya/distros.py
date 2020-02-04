def common_distr():
    return [
        'superbox',
        'mc-slang',
        'yash',
        'bash',
        'dash',
        'p7zip',
        'unrar',
        'bsdtar',
        'python3',
        'xz',
        'cmake',
        'curl',
        'bzip2',
        'openssl',
        'gzip',
        'grep',
        'gawk',
        'sed',
        'sqlite3',
        'file',
    ]


def distr_by_name(name):
    return eval('y.' + name + '_distr')


def all_distros():
    return common_distr()
