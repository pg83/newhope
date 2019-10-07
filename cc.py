import hashlib
import json


V = {
    'common': {
        'kind': 'c/c++ compiler',
        'build': [
            'wget -O - $(URL) | tar --strip-components 2 -xzf - ',
        ],
        "prepare": [
            "export PATH=`cwd`/bin:$PATH",
            'export LDFLAGS=--static',
            'export CFLAGS=-I`cwd`/include',
        ],
    },
    "barebone": [
        {
            "url": "https://musl.cc/x86_64-linux-musl-native.tgz",
            "constraints": [
                {
                    "libc": 'musl',
                    'arch': 'x86_64',
                },
                {
                    'arch': 'x86_64',
                },
            ],
        },
        {
            "url": "https://musl.cc/aarch64-linux-musl-native.tgz",
            "constraints": [
                {
                    "libc": 'musl',
                    'arch': 'aarch64',
                },
                {
                    'arch': 'aarch64',
                },
            ],
        },
        {
            "url": "https://musl.cc/aarch64-linux-musl-native.tgz",
            "constraints": [
                {
                    "libc": 'musl',
                    'target': 'aarch64',
                    'host': 'x86_64',
                },
                {
                    'target': 'aarch64',
                    'host': 'x86_64',
                },
            ],
        },
    ],
}


def iter_comp():
    for c in json.loads(json.dumps(V['barebone'])):
        cc = c.pop('constraints')

        for ccc in cc:
            v = json.loads(json.dumps(c))

            v['constraint'] = json.loads(json.dumps(ccc))
            v['name'] = 'gcc'
            v['version'] = '9.2'

            vc = v['constraint']

            if 'arch' in vc:
                arch = vc.pop('arch')

                vc['target'] = arch
                vc['host'] = arch

            v.update(V['common'])

            if 'libc' in v['constraint']:
                v['id'] = hashlib.md5(json.dumps(v, indent=4, sort_keys=True)).hexdigest()

            yield json.loads(json.dumps(v))


res = list(iter_comp())
