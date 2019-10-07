import json

from gen_id import gen_id


V = {
    'common': {
        'kind': 'c/c++ compiler',
        'build': [
            'wget -O - $(URL) | tar --strip-components 2 -xzf - ',
        ],
        "prepare": [
            "export PATH=`pwd`/bin:$PATH",
            'export LDFLAGS=--static',
            'export CFLAGS=-I`cwd`/include',
        ],
    },
    "barebone": [
        {
            'prefix': ['tool_native_prefix', 'x86_64-linux-musl-'],
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
            'prefix': ['tool_native_prefix', 'aarch64-linux-musl-'],
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
            'prefix': ['tool_cross_prefix', 'aarch64-linux-musl-'],
            "url": "https://musl.cc/aarch64-linux-musl-cross.tgz",
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

            v.update(json.loads(json.dumps(V['common'])))
            v['prepare'].append('export ' + v['prefix'][0].upper() + '=' + v['prefix'][1])

            if 'libc' in v['constraint']:
                v['id'] = gen_id(v)

            yield json.loads(json.dumps(v))


res = list(iter_comp())
