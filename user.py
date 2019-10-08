from all import find_compiler
from gen_id import gen_id
from bb import find_busybox


def find_compiler_id(*args, **kwargs):
    for x in find_compiler(*args, **kwargs):
        return x['id']

    raise Exception('shit happen')


def gen_bb(src, target='aarch64', libc='musl'):
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


def gen_musl(src, target='aarch64'):
    res = {
        'deps': [
            find_compiler_id(target='x86_64', host='x86_64', libc='musl'),
            find_compiler_id(target=target, host='x86_64', libc='musl'),
        ],
        'build': [
            'export MY_CWD=`pwd`'
            'mkdir build',
            'cd build',
            'wget -O - $(URL) | tar --strip-components 1 -xjf -',
            'export CFLAGS=-O2',
            'export CROSS_COMPILE=$TOOL_CROSS_PREFIX',
            './configure --prefix=/ --enable-static --disable-shared',
            'make',
            'make DESTDIR=$MY_CWD install',
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


def gen_tb(src, target='aarch64'):
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


USER_PACKAGES = [
    gen_bb('https://www.busybox.net/downloads/busybox-1.30.1.tar.bz2'),
    gen_tb('http://landley.net/toybox/downloads/toybox-0.8.1.tar.gz'),
    #gen_musl('https://www.musl-libc.org/releases/musl-1.1.23.tar.gz', target='aarch64'),
    #gen_musl('https://www.musl-libc.org/releases/musl-1.1.23.tar.gz', target='x86_64'),
]
