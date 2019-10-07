import hashlib
import json
import os


V = {
    "deepmerge": {
        'kind': 'sysutils',
        "name": "busybox",
        "use": [
            "mkdir xbin_$(ARCH)",
            "busybox-$(ARCH) --install xbin_$(ARCH)/",
            "PATH=xbin_$(ARCH)/:$PATH",
        ],
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

        if arch not in v1['url']:
            app = ['mv ' + os.path.basename(v1['url']) + ' ' + 'busybox-' + arch]
        else:
            app = []

        v1['constraint']['host'] = arch
        v1['constraint']['target'] = arch

        v1.update(v2)

        v1['use'] = app + ['chmod +x busybox-' + arch] + [x.replace('$(ARCH)', arch) for x in v1['use']]
        v1['version'] = os.path.basename(os.path.dirname(v1['url'])).split('-')[0]
        v1['id'] = hashlib.md5(json.dumps(v1, sort_keys=True)).hexdigest()

        yield v1


res = list(iter_constraints())
