import json

from upm import gen_id


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
        l = json.loads(json.dumps(l))

        l['build'] = json.loads(json.dumps(V['build']))
        l['from'] = __file__

        yield {
            'node': l,
            'deps': [],
        }
