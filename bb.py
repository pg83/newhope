import json
import os


V = {
    "deepmerge": {
        'kind': 'sysutils',
        "name": "busybox",
        "prepare": [
            "mkdir xbin",
            "ln -s ./$(BB) ./xbin/",
            "./xbin/$(BB) --install ./xbin",
            "export PATH=`pwd`/xbin/:$PATH",
        ],
        "build": [
            "wget -O $(BB) $(URL)",
            'chmod +x ./$(BB)',
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

        v1.update(v2)

        def repl_list(l):
            return [x.replace('$(BB)', 'busybox-$(ARCH)').replace('$(ARCH)', arch) for x in l]

        v1['prepare'] = repl_list(v1['prepare'])
        v1['build'] = repl_list(v1['build'])

        v1['version'] = os.path.basename(os.path.dirname(v1['url'])).split('-')[0]

        yield v1


res = list(iter_constraints())


def find_busybox(host, target):
    for c in res:
        c = json.loads(json.dumps(c))

        if c['constraint']['target'] == target:
            if host != target:
                c['deps'] = c.get('deps', []) + [find_busybox(host, host)]

            return c

    raise Exception('no busybox for %s' % host)
