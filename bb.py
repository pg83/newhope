import json
import os
import gen_id


V = {
    "deepmerge": {
        'kind': 'sysutils',
        'name': 'busybox1',
        "prepare": [
            "mkdir $(BUSYBOX1_BIN_DIR)",
            "cd $(BUSYBOX1_BIN_DIR)",
            "../original/$(BB) --install -s $(BUSYBOX1_BIN_DIR)",
        ],
        "build": [
            '#pragma manual deps',
            'mkdir $(INSTALL_DIR)/original',
            'wget -O $(INSTALL_DIR)/original/$(BB) $(URL)',
            'chmod +x $(INSTALL_DIR)/original/$(BB)',
        ],
        "from": __file__,
    },
    "barebone": [
        {
	    "url": "https://www.busybox.net/downloads/binaries/1.31.0-defconfig-multiarch-musl/busybox-armv8l",
	    "constraint": {
                "libc": "musl",
                "arch": "aarch64",
            },
        },
        {
	    "url": "https://www.busybox.net/downloads/binaries/1.31.0-defconfig-multiarch-musl/busybox-x86_64",
	    "constraint": {
                "libc": "musl",
                "arch": "x86_64",
            },
        },
    ],
}


def iter_constraints():
    for x in V['barebone']:
        v1 = json.loads(json.dumps(x))
        v2 = json.loads(json.dumps(V['deepmerge']))
        arch = v1['constraint'].pop('arch')
        
        v1['constraint']['host'] = arch
        v1['constraint']['target'] = arch
        v1['constraint']['build_system_version'] = gen_id.cur_build_system_version()

        v1.update(v2)

        def repl_list(l):
            return [x.replace('$(BB)', 'busybox-$(ARCH)').replace('$(ARCH)', arch) for x in l]

        v1['prepare'] = repl_list(v1['prepare'])
        v1['build'] = repl_list(v1['build'])
        v1['version'] = os.path.basename(os.path.dirname(v1['url'])).split('-')[0]

        yield {
            'node': v1,
            'deps': [],
        }


def find_busybox(host, target):
    for c in iter_constraints():
        if c['node']['constraint']['target'] == target:
            return gen_id.deep_copy(c)

    raise Exception('no busybox for %s' % host)
