V = [
    {
        'kind': 'libc-source',
        'url': 'https://www.uclibc.org/downloads/snapshots/uClibc-snapshot.tar.bz2',
        'name': 'uclibc',
        "build": [
            '$(FETCH_URL)',
        ],
    },
    {
        'kind': 'libc-source',
        'url': 'https://www.musl-libc.org/releases/musl-1.1.23.tar.gz',
        'name': 'musl',
        "build": [
            '$(FETCH_URL)',
        ],
    },
]



def iter_libc():
    for l in V['barebone']:
        yield l

