import os
import sys

def fp(f, v, *args, **kwargs):
    def wrap(*args, **kwargs):
        return f(v, *args, **kwargs)

    return wrap

from all import find_compiler, RES
from gen_id import gen_id
from bb import find_busybox
from build import to_visible_name, get_pkg_link


def find_compiler_id(*args, **kwargs):
    for x in find_compiler(*args, **kwargs):
        return x['id']

    raise Exception('shit happen')


def helper(func):
    def wrapper(src, target='aarch64', host='x86_64', libc='musl'):
        def iter_compilers():
            if target == host:
                yield find_compiler_id(target=target, host=host, libc=libc)
            else:
                yield find_compiler_id(target=host, host=host, libc=libc)
                yield find_compiler_id(target=target, host=host, libc=libc)

        fetch_url = 'wget -O - $(URL) | tar --strip-components 1 -x#f - ;'

        if '.bz2' in src:
            fetch_url = fetch_url.replace('#', 'j')
        else:
            fetch_url = fetch_url.replace('#', 'z')

        data = func()

        res = {
            'deps': list(iter_compilers()),
            'build': ['cd $(BUILD_DIR)'] + [x.strip() for x in data.replace('$(FETCH_URL)', fetch_url).split('\n')],
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
def tb():
    return """
        $(FETCH_URL)
        LDFLAGS=--static CFLAGS=-O2 CC=gcc CROSS_COMPILE=$TOOL_CROSS_PREFIX make defconfig toybox
        mv toybox $(INSTALL_DIR)"""


@helper
def m4():
    return '$(FETCH_URL) ./configure --prefix=$(INSTALL_DIR) && make && make install'


@helper
def xz():
    return '$(FETCH_URL) ./configure --prefix=$(INSTALL_DIR) --disable-shared --enable-static && make && make install'


@helper
def bb():
    return """
        $(FETCH_URL)
        make CROSS_COMPILE=$TOOL_CROSS_PREFIX defconfig
        make CROSS_COMPILE=$TOOL_CROSS_PREFIX
        mv busybox $(INSTALL_DIR)/
    """


@helper
def musl():
    return """
        $(FETCH_URL)
        LDFLAGS=--static CFLAGS=-O2 CROSS_COMPILE=$TOOL_CROSS_PREFIX ./configure --prefix=$(INSTALL_DIR) --enable-static --disable-shared && make && make install
    """


@helper
def ncurses():
    return """
        $(FETCH_URL)
        sed -i s/mawk// configure
        ./configure --prefix=$(INSTALL_DIR) --without-shared --without-debug --without-ada --enable-widec --enable-overwrite &?&? make && make        install"""


@helper
def pkg_config():
    return """
        $(FETCH_URL)
        LDFLAGS=--static ./configure --prefix=$(INSTALL_DIR) --with-internal-glib --enable-static --disable-shared && make && make install
    """


@helper
def tar():
    return """
        $(FETCH_URL) FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=$(INSTALL_DIR) && make && make install
    """


USER_PACKAGES_1 = [
    #fp(tb, 'http://landley.net/toybox/downloads/toybox-0.8.1.tar.gz'),
    fp(bb, 'https://www.busybox.net/downloads/busybox-1.30.1.tar.bz2'),
    fp(musl, 'https://www.musl-libc.org/releases/musl-1.1.23.tar.gz'),
    fp(m4, 'https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz'),
    fp(xz, 'https://tukaani.org/xz/xz-5.2.4.tar.gz'),
    fp(tar, 'https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz'),
    fp(pkg_config, 'https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz'),
    #fp(ncurses, 'https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz'),
]

USER_PACKAGES = [x(target='x86_64') for x in USER_PACKAGES_1] + [x(target='aarch64') for x in USER_PACKAGES_1]

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


def install_xz():
    p1 = USER_PACKAGES[3]
    p2 = USER_PACKAGES[4]



    l1 = get_pkg_link(to_visible_name(p1))
    l2 = get_pkg_link(to_visible_name(p2))

    os.environ['PATH'] = l1 + '/bin:' + l2 + '/bin:' + os.environ['PATH']

    print >>sys.stderr, os.environ['PATH']
