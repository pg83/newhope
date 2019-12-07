def gen_fetch_cmd(url):
    fname = y.calc_pkg_full_name(url)
    cache = '$SD/' + fname

    return {
        'inputs': [],
        'output': cache,
        'build': [
            '$UPM fetchurl "' + url + '" "' + cache + '"'
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


def fix_v2(v, **kwargs):
    assert v is not None

    v = y.deep_copy(v)
    n = v['node']

    m = y.ensure_value('meta', n, {})
    f = y.ensure_value('flags', m, [])
    
    m['flags'] = sorted(frozenset(f + n.pop('flags', [])))

    kind = y.ensure_value('kind', m, []) + n.pop('kind', [])
    m['kind'] = kind
    
    if 'box' in kind:
        kind.append('tool')
        
    if 'compression' in kind:
        kind.append('tool')

    if 'provides' in m:
        kind.append('library')

    m['kind'] = sorted(frozenset(kind))
        
    f = m['flags']
    
    if n.get('codec', '') == 'tr':
        pass
    else:
        if 'compression' in kind:
            n['codec'] = 'gz'
        elif 'HAVE_7ZA_BIN' in f:
            n['codec'] = '7z'
        elif 'HAVE_XZ_BIN' in f:
            n['codec'] = 'xz'
        else:
            n['codec'] = kwargs.get('codec', 'gz')

    if 'naked' in kwargs:
        n['naked'] = kwargs['naked']

    if 'url' in n:
        if 'pkg_full_name' not in n:
            n['pkg_full_name'] = y.calc_pkg_full_name(n['url'])

    for p in ('build', 'prepare'):
        if p in n:
            n[p] = list(apply_fetch(n[p], v))

    return v
