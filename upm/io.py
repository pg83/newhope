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
        ('.zip', 'zp'),
    ]

    if '-tr-' in name:
        return 'tr'

    for k, v in lst:
        if name.endswith(k):
            return v

    if '-xz-' in name:
        return 'xz'

    if '-zp-' in name:
        return 'zp'

    if '-gz-' in name:
        return 'gz'

    if '-bz-' in name:
        return 'bz'

    raise Exception('shit happen ' + name)


def known_codecs():
    return ('xz', 'gz', 'tr', 'bz', 'zp')


def prepare_tar_cmd(fr, to, codec=None):
    res = {
        'xz': '$YXZ -zc',
        'gz': '$YGZIP -c',
        'tr': 'cat',
        'bz': '$YBZIP2 -c',
    }

    if not codec:
        codec = calc_mode(os.path.basename(to))

    if codec == 'zp':
        return

    def iter_lines():
        if fr == '"$1"':
            dr = '$(dirname "$2")'
        else:
            dr = os.path.dirname(to)

        assert dr

        yield 'mkdir -p ' + dr
        yield 'cd ' + fr
        yield '($YTAR -v -cf - . | ' + res[codec] + ')'

    yield '((' + ' && '.join(iter_lines()) + ') > ' + to + '-tmp) && (mv ' + to + '-tmp ' + to + ')'


@y.singleton
def gen_extra_scripts():
    def do():
        for codec in known_codecs():
            data = ''.join(prepare_tar_cmd('"$1"', '"$2"', codec))

            yield 'prepare_' + codec + '_pkg', data

        for codec in list(known_codecs()) + ['zp']:
            data = ''.join(prepare_untar_cmd('"$1"', '.', ext_mode=codec, rm_old=False, extra='--strip-components $2'))

            yield 'untar_' + codec, data

    return list(do())


def prepare_untar_for_mf(fr, strip=0):
    return 'source untar_{codec} "{file}" {strip}'.format(codec=calc_mode(os.path.basename(fr)), file=fr, strip=strip)


def prepare_untar_cmd(fr, to, extra='', rm_old=True, ext_mode=None):
    if (ext_mode and ext_mode == 'zp') or fr.endswith('.zip'):
        def do():
            yield '$YUNZIP ' + fr

            if to not in ' .':
                yield 'cd ' + to
                yield 'mkdir -p ' + to

                if rm_old:
                    yield '(rm -rf ' + to + ' || true)'

        return ' && '.join(reversed(list(do())))

    tbl = {
        'xz': '| $YXZ --decompress --stdout |',
        'gz': '| $YGZIP -dc |',
        'bz': '| $YBZIP2 -dc |',
        'tr': '|',
    }

    mode = ext_mode or calc_mode(os.path.basename(fr))
    core = 'cat {fr} {uncompress} $YTAR {extra} -xf -'.format(fr=fr, uncompress=tbl[mode], extra=extra)

    if to in ' .':
        return core

    bt_rm = {
        True: '(rm -rf {to} || true) && ',
        False: '',
    }

    return (bt_rm[rm_old] + '(mkdir -p {to}) && (cd {to}) && ({core})').format(to=to, core=core)
