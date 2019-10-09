import json


V = {
    'common': {
        'kind': 'c/c++ compiler',
        'build': [
            'cd $(INSTALL_DIR)',
            'export PATH=$(TAR_BIN_DIR):$(XZ_BIN_DIR):$PATH',
            'time wget -O - $(URL) | tar --strip-components 2 -xzf - ',
        ],
        "prepare": [
            "export PATH=`pwd`/bin:$PATH",
            'export LDFLAGS=--static',
            'export CFLAGS=-I`pwd`/include',
        ],
        "from": __file__,
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

            p1 = v['prefix'][0]
            p2 = v['prefix'][1]

            v['prepare'].append('export ' + p1.upper() + '=' + p2)

            yield json.loads(json.dumps(v))


res = list(iter_comp())
