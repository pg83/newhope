import json

from upm import gen_id


V = {
    'common': {
        'kind': 'c/c++ compiler',
        'build': [
            '#pragma manual deps',
            '$(FETCH_URL_2)',
            'rm -rf $(BUILD_DIR)/fetched_urls',
            'mv $(BUILD_DIR)/* $(INSTALL_DIR)/'
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
            v['constraint']['build_system_version'] = gen_id.cur_build_system_version()

            vc = v['constraint']

            if 'arch' in vc:
                arch = vc.pop('arch')

                vc['target'] = arch
                vc['host'] = arch

            v['name'] = 'gcc' + vc['host'][0] + vc['target'][0]
            v['version'] = '9.2'

            v.update(json.loads(json.dumps(V['common'])))

            p1 = v['prefix'][0]
            p2 = v['prefix'][1]

            name = v['name'].upper() + '_BIN_DIR'

            v['prepare'] = [
                'export PATH=$(' + name + '):$PATH',
                'export LDFLAGS=--static',
                'export CFLAGS=-I$(' + name + ')',
                'export ' + p1.upper() + '=' + p2,
            ]

            yield {
                'node': json.loads(json.dumps(v)),
                'deps': [],
            }


def find_compiler(info):
    for node in iter_comp():
        c = node['node']['constraint']
        ok = 0

        for k, v in info.items():
            if c.get(k, '') == v:
                ok += 1

        if ok == len(info):
            yield gen_id.deep_copy(node)
