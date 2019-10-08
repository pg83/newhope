import os
import sys

from all import find_compiler, RES
from gen_id import gen_id
from bb import find_busybox
from build import to_visible_name


def find_compiler_id(*args, **kwargs):
    for x in find_compiler(*args, **kwargs):
        return x['id']

    raise Exception('shit happen')



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

        res = {
            'deps': list(iter_compilers()),
            'build': ['cd $(BUILD_DIR)'] + [x.strip() for x in func().split('\n')],
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
    wget -O - $(URL) | tar --strip-components 1 -xzf -
    ./configure --prefix=$(INSTALL_DIR) && make && make install
"""


@helper
def xz():
    return """
    wget -O - $(URL) | tar --strip-components 1 -xzf -
    ./configure --prefix=$(INSTALL_DIR) --disable-shared --enable-static && make && make install
"""


@helper
def bb():
    return """
        wget -O - $(URL) | tar --strip-components 1 -xjf -
        make CROSS_COMPILE=$TOOL_CROSS_PREFIX defconfig
        make CROSS_COMPILE=$TOOL_CROSS_PREFIX
        mv busybox $(INSTALL_DIR)/
    """


@helper
def musl():
    return """
        wget -O - $(URL) | tar --strip-components 1 -xjf -
        LDFLAGS=--static CFLAGS=-O2 CROSS_COMPILE=$TOOL_CROSS_PREFIX ./configure --prefix=$(INSTALL_DIR) --enable-static --disable-shared && make && make install
    """


@helper
def ncurses():
    return """
    wget -O - $(URL) | tar --strip-components 1 -xzf -
    sed -i s/mawk// configure
    LDFLAGS=--static ./configure --prefix=$(INSTALL_DIR) --without-shared --without-debug --without-ada --enable-widec --enable-overwrite &?&? make && make install
    """


@helper
def pkg_config():
    return """
    wget -O - $(URL) | tar --strip-components 1 -xzf -
    LDFLAGS=--static ./configure --prefix=$(INSTALL_DIR) --with-internal-glib --enable-static --disable-shared && make && make install
    """

USER_PACKAGES = [
    pkg_config('https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz', target='x86_64'),
    pkg_config('https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz', target='aarch64'),
    ncurses('https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz', target='x86_64'),
    ncurses('https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz', target='aarch64'),
    bb('https://www.busybox.net/downloads/busybox-1.30.1.tar.bz2', target='x86_64'),
    bb('https://www.busybox.net/downloads/busybox-1.30.1.tar.bz2', target='aarch64'),
    tb('http://landley.net/toybox/downloads/toybox-0.8.1.tar.gz'),
    musl('https://www.musl-libc.org/releases/musl-1.1.23.tar.gz', target='aarch64'),
    musl('https://www.musl-libc.org/releases/musl-1.1.23.tar.gz', target='x86_64'),
    m4('https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz'),
    xz('https://tukaani.org/xz/xz-5.2.4.tar.gz', target='x86_64'),
    xz('https://tukaani.org/xz/xz-5.2.4.tar.gz', target='aarch64'),
]


ALL_PACKAGES = RES + USER_PACKAGES


def prune_repo():
    files = set()

    for x in ALL_PACKAGES:
        if 'id' in x:
            files.add(to_visible_name(x))
        else:
            print >>sys.stderr, 'unfinished', x

    for l in os.listdir('/repo/'):
        if l not in files:
            l = '/repo/' + l

            print >>sys.stderr, 'prune', l

            os.unlink(l)
