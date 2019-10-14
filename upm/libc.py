from .gen_id import deep_copy


V = {
    "build": [
        '$(FETCH_URL)',
    ],
    "barebone": [
        {
            'kind': 'libc-source',
            'url': 'https://www.uclibc.org/downloads/snapshots/uClibc-snapshot.tar.bz2',
            'name': 'uclibc',
        },
        {
            'kind': 'libc-source',
            'url': 'https://www.musl-libc.org/releases/musl-1.1.23.tar.gz',
            'name': 'musl',
        },
    ],
}


def iter_libc():
    for l in V['barebone']:
        l = deep_copy(l)

        l['build'] = deep_copy(V['build'])
        l['from'] = __file__

        yield {
            'node': l,
            'deps': [],
        }
