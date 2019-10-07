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
