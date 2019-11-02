import hashlib


def apply_fetch(lines, v):
    for l in lines:
        if 'source fetch ' in l:
            parts = l.split('"')

            assert len(parts) == 3

            url = parts[1]
            id = y.gen_fetch_node_3(url, hashlib.md5(url).hexdigest(), v['deps'])
            v['deps'] = v['deps'] + [id]
            n = y.restore_node_node(id)

            yield y.prepare_untar_for_mf(n['file'], strip=int(parts[2].strip()))
        else:
            yield l


def fix_v2(v, **kwargs):
    assert v is not None

    v = y.deep_copy(v)

    n = v['node']

    if 'codec' not in n:
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

