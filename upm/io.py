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
        ('-xz', 'xz'),
        ('-gz', 'gz'),
        ('-bz', 'bz'),
        ('-zp', 'zp'),
        ('-tr', 'tr'),
        ('-7z', '7z'),
        ('-pg', 'pg'),
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
    return ('xz', 'gz', 'tr', 'bz', 'zp', '7z', 'pg')


def prepare_tar_cmd(fr, to, codec=None):
    res = {
        'xz': '$YXZ -zc',
        'gz': '$YGZIP -c',
        'tr': 'cat',
        'bz': '$YBZIP2 -c',
        '7z': '$Y7ZA a -si {to}',
        'pg': '$SD/upm cmd codec -c',
    }

    if not codec:
        codec = calc_mode(y.os.path.basename(to))

    if codec == 'zp':
        return

    def iter_lines():
        if fr == '"$1"':
            dr = '$(dirname "$2")'
        else:
            dr = y.os.path.dirname(to)

        assert dr

        yield 'mkdir -p ' + dr
        yield 'cd ' + fr
        yield '($YTAR -v -cf - . | ' + res[codec] + ')'

    if codec == '7z':
        tot = to + '-tmp.7z'
        
        yield ('(' + ' && '.join(iter_lines()) + ') && (mv {to} ' + to + ')').replace('{to}', tot)
    else:
        yield '((' + ' && '.join(iter_lines()) + ') > ' + to + '-tmp) && (mv ' + to + '-tmp ' + to + ')'

        
data1 = '''
if test $2 -eq 1; then
    q=$(basename $1)
    q=$(echo $q | tr '_' '-' | tr '.' '-' | tr '-' '\n' | head -n 1)
    mv ./$q* ./xxx
    mv ./xxx/* ./
    rm -rf ./xxx
fi
'''


@y.singleton
def gen_extra_scripts():
    def do():
        for codec in known_codecs():
            data = ''.join(prepare_tar_cmd('"$1"', '"$2"', codec))

            yield 'prepare_' + codec + '_pkg', data

        for codec in list(known_codecs()) + ['zp']:
            data = ''.join(prepare_untar_cmd('"$1"', '.', ext_mode=codec, rm_old=False))
            yield 'untar_' + codec, data + '\n' + data1

    return list(do())


def prepare_untar_for_mf(fr, strip=0):
    try:
        return 'source untar_{codec} "{file}" {strip}'.format(codec=calc_mode(y.os.path.basename(fr)), file=fr, strip=strip)
    except Exception:
        return 'cp "{file}" .'.format(file=fr)
    

def prepare_untar_cmd(fr, to, extra='', rm_old=True, ext_mode=None):
    if (ext_mode and ext_mode == 'zp') or fr.endswith('.zip'):
        def do():
            yield '$YUNZIP -o ' + fr

            if to not in ' .':
                yield 'cd ' + to
                yield 'mkdir -p ' + to

                if rm_old:
                    yield '(rm -rf ' + to + ' || true)'

        return ' && '.join(reversed(list(do())))

    tbl = {
        'xz': '| $YXZCAT -f |',
        'gz': '| $YGZIP -dc |',
        'bz': '| $YBZIP2 -dc |',
        'pg': '| $SD/upm cmd codec -d |',
        'tr': '|',
    }

    mode = ext_mode or cay.lc_mode(os.path.basename(fr))

    if mode == '7z':
        core = '$Y7ZA x -so {fr} | $YTAR {extra} -xf -'.format(fr=fr, extra=extra)
    else:
        core = 'cat {fr} {uncompress} $YTAR {extra} -xf -'.format(fr=fr, uncompress=tbl[mode], extra=extra)

    if to in ' .':
        return core

    bt_rm = {
        True: '(rm -rf {to} || true) && ',
        False: '',
    }

    return (bt_rm[rm_old] + '(mkdir -p {to}) && (cd {to}) && ({core})').format(to=to, core=core)
