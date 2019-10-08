import json


V = {
    "build": [
        'mkdir .build',
        'cd .build',
        'wget $(URL)',
        'tar -xf *',
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
        l = json.loads(json.dumps(l))
        l['build'] = json.loads(json.dumps(V['build']))

        yield l


res = list(iter_libc())
