import os


def calc_mode(name):
    lst = [
        ('.xz', 'xz'),
        ('.txz', 'xz'),
        ('.gz', 'gz'),
        ('.tgz', 'gz'),
        ('.tar', 'tr'),
        ('.bz2', 'bz'),
        ('.tbz2', 'bz'),
        ('.tbz', 'bz'),
    ]

    for k, v in lst:
        if name.endswith(k):
            return v

    if '-xz-' in name:
        return 'xz'

    if '-gz-' in name:
        return 'gz'

    if '-bz-' in name:
        return 'bz'

    if '-tr-' in name:
        return 'tr'

    raise Exception('shit happen ' + name)


def prepare_tar_cmd(fr, to, codec=None):
    res = {
        'xz': 'xz -zc',
        'gz': 'gzip -c',
        'tr': 'cat',
        'bz': 'bzip2 -c',
    }

    if not codec:
        codec = calc_mode(os.path.basename(to))

    def iter_lines():
        if to == '$(PKG_FILE)':
            dr = '$(WDR)'
        else:
            dr = os.path.dirname(to)

        assert dr

        yield 'mkdir -p ' + dr
        yield 'cd ' + fr
        yield '(tar -v -cf - . | ' + res[codec] + ')'

    yield '(' + ' && '.join(iter_lines()) + ' > ' + to + '-tmp) && (mv ' + to + '-tmp ' + to + ')'


def prepare_untar_cmd(fr, to, extra='', rm_old=True):
    if fr.endswith('.zip'):
        def do():
            yield 'unzip ' + fr

            if to not in ' .':
                yield 'cd ' + to
                yield 'mkdir -p ' + to

                if rm_old:
                    yield '(rm -rf ' + to + ' || true)'

        return ' && '.join(do())

    tbl = {
        'xz': '| xz --decompress --stdout |',
        'gz': '| gzip -d |',
        'bz': '| bzip2 -d |',
        'tr': '|',
    }

    mode = calc_mode(os.path.basename(fr))
    core = 'cat {fr} {uncompress} tar {extra} -v -xf -'.format(fr=fr, uncompress=tbl[mode], extra=extra)

    if to in ' .':
        return core

    bt_rm = {
        True: '(rm -rf {to} || true) && ',
        False: '',
    }

    return (bt_rm[rm_old] + '(mkdir -p {to}) && (cd {to}) && ({core})').format(to=to, core=core)
