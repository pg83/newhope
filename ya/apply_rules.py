def gen_fetch_cmd(url):
    fname = y.calc_pkg_full_name(url)
    cache = '$SD/' + fname

    return {
        'inputs': [],
        'output': cache,
        'build': [
            'PYTHONHOME= $SD/upm cmd fetch "' + url + '" "' + cache + '"'
        ],
    }


def apply_fetch(lines, v):
    for l in lines:
        if 'source fetch ' in l:
            parts = l.split('"')

            assert len(parts) == 3

            url = parts[1]
            bn = gen_fetch_cmd(url)
            vn = v['node']

            y.prepend_list('extra_cmd', vn, bn)
            y.prepend_list('urls', vn, url)

            yield y.prepare_untar_for_mf(bn['output'], strip=int(parts[2].strip()))
        else:
            yield l


def fix_v2(v):
    assert v is not None

    v = y.dc(v)
    n = v['node']

    m = y.ensure_value('meta', n, {})
    f = y.ensure_value('flags', m, [])

    m['flags'] = sorted(frozenset(f + n.pop('flags', [])))

    kind = y.ensure_value('kind', m, []) + n.pop('kind', [])
    m['kind'] = kind

    if 'box' in kind:
        kind.append('tool')

    if 'provides' in m and any(('lib' in x) for x in m['provides']):
        kind.append('library')

    m['kind'] = sorted(frozenset(kind))
    f = m['flags']

    if 'codec' not in n:
        n['codec'] = 'pg'

    def iter_subst():
        for i, v in enumerate(n.get('extra', [])):
            if v['kind'] == 'file':
                cmd = 'echo "' + y.base64.b64encode(v['data'].encode('utf-8')).decode('utf-8') + '" | source base64_decode > ' + v['path']
                key = '$(F_' + str(i) + ')'

                yield (key, cmd)

            if v['kind'] == 'subst':
                yield (v['from'], v['to'])

    subst = list(iter_subst())

    for p in ('build', 'prepare'):
        if p in n:
            n[p] = [y.subst_kv_base(l, subst) for l in apply_fetch(n[p], v)]

    return v


def subst_kv_base(data, *iterables):
    for k, v in y.itertools.chain(*iterables):
        data = data.replace(k, v)

    return data
