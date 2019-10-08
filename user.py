import os

from all import find_compiler
from gen_id import gen_id
from bb import find_busybox


def find_compiler_id(*args, **kwargs):
    for x in find_compiler(*args, **kwargs):
        return x['id']

    raise Exception('shit happen')


def bb(src, target='aarch64', libc='musl'):
    res = {
        'deps': [
            find_compiler_id(target='x86_64', host='x86_64', libc=libc),
            find_compiler_id(target=target, host='x86_64', libc=libc),
        ],
        'build': [
            'mkdir build',
            'cd build',
            'wget -O - $(URL) | tar --strip-components 1 -xjf -',
            'make CROSS_COMPILE=$TOOL_CROSS_PREFIX defconfig',
            'make CROSS_COMPILE=$TOOL_CROSS_PREFIX',
            'mv busybox ..',
            'cd ..',
            'rm -rf build',
        ],
        "url": src,
        "constraint": {
            "libc": libc,
            "host": 'x86_64',
            'target': target,
        },
    }

    res['id'] = gen_id(res)

    return res


def musl(src, target='aarch64'):
    res = {
        'deps': [
            find_compiler_id(target='x86_64', host='x86_64', libc='musl'),
            find_compiler_id(target=target, host='x86_64', libc='musl'),
        ],
        'build': [
            'mkdir build',
            'cd build',
            'wget -O - $(URL) | tar --strip-components 1 -xjf -',
            'LDFLAGS=--static CFLAGS=-O2 CROSS_COMPILE=$TOOL_CROSS_PREFIX ./configure --prefix=/private/musl-1.1.21 --enable-static --disable-shared && make',
        ],
        "url": src,
        "constraint": {
            "libc": 'musl',
            "host": 'x86_64',
            'target': target,
        },
    }

    res['id'] = gen_id(res)

    return res


def tb(src, target='aarch64'):
    res = {
        'deps': [
            find_compiler_id(target='x86_64', host='x86_64', libc='musl'),
            find_compiler_id(target=target, host='x86_64', libc='musl'),
        ],
        'build': [
            'mkdir build',
            'cd build',
            'wget -O - $(URL) | tar --strip-components 1 -xzf -',
            'LDFLAGS=--static CFLAGS=-O2 CC=gcc CROSS_COMPILE=$TOOL_CROSS_PREFIX make defconfig toybox',
            'mv toybox ..',
            'cd ..',
        ],
        "url": src,
        "constraint": {
            "libc": 'musl',
            "host": 'x86_64',
            'target': target,
        },
    }

    res['id'] = gen_id(res)

    return res


def helper(func):
    def wrapper(src, target='aarch64', host='x86_64', libc='musl'):
        def iter_compilers():
            if target == host:
                yield find_compiler_id(target=target, host=host, libc=libc)
            else:
                yield find_compiler_id(target=host, host=host, libc=libc)
                yield find_compiler_id(target=target, host=host, libc=libc)

        ver = os.path.basename(src)

        res = {
            'deps': list(iter_compilers()),
            'build': [x.strip() for x in func().replace('$(VERSION)', ver).replace('$(URL)', src).split('\n')],
            "url": src,
            "constraint": {
                "libc": libc,
                "host": host,
                'target': target,
            },
        }

        res['id'] = gen_id(res)

        return res

    return wrapper


@helper
def m4():
    return """
    mkdir build
    cd build
    wget $(URL)
    ./configure --prefix=/private/$(VERSION) --disable-shared --enable-static
    make
    make install
"""


USER_PACKAGES = [
    bb('https://www.busybox.net/downloads/busybox-1.30.1.tar.bz2'),
    tb('http://landley.net/toybox/downloads/toybox-0.8.1.tar.gz'),
    musl('https://www.musl-libc.org/releases/musl-1.1.23.tar.gz'),
    m4('https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz'),
]
